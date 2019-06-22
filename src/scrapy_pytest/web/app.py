from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_paginate import Pagination, get_page_parameter, get_per_page_parameter

from ..mock import mock_spidercls
from ..utils.request import request_from_dict
from .config import DevelopmentConfig
from .common import save_data, delete_cache
from .exts import db
from .models import Request, Storage, Spider, ParseFunc

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()


@app.template_filter('loads_url')
def loads_meta(value):
    return value['url']


@app.template_filter('loads_meta')
def loads_meta(value):
    return value['meta']


@app.route('/')
def home():
    save_data()
    page = request.args.get(get_page_parameter(), default=1, type=int)
    per_page = request.args.get(get_per_page_parameter(), default=15, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    total = Request.query.count()
    reqs = Request.query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=total, per_page=per_page)

    distinct_storage = Storage.query.with_entities(Storage.name).distinct().all()
    distinct_spider = Spider.query.with_entities(Spider.name).distinct().all()
    return render_template('index.html',
                           **{'reqs': reqs, 'pagination': pagination, 'distinct_storage': distinct_storage,
                              'distinct_spider': distinct_spider})


@app.route('/filter')
def filter_req():
    PER_PAGE = 15
    save_data()
    storage = request.args.get('storage', 'all')
    spider = request.args.get('spider', 'all')
    page = request.args.get(get_page_parameter(), default=1, type=int)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    if storage.strip() == 'all':
        total = Request.query.count()
        reqs = Request.query.slice(start, end)
    else:
        total = Request.query.join(Storage, Storage.id == Request.storage_id).filter(Storage.name == storage).count()
        reqs = Request.query.join(Storage, Storage.id == Request.storage_id).filter(Storage.name == storage).slice(
            start, end)
    rows = []
    for req in reqs:
        if spider.strip() == 'all':
            rows.append(dict(
                id=req.id,
                storage=req.storage.name,
                spider=req.spider.name,
                parse_func=req.parse_func.name,
                url=req.data['url'],
                meta=req.data['meta']
            ))
        else:
            if req.spider.name == spider:
                rows.append(dict(
                    id=req.id,
                    storage=req.storage.name,
                    spider=req.spider.name,
                    parse_func=req.parse_func.name,
                    url=req.data['url'],
                    meta=req.data['meta']
                ))
    return jsonify(**{
        'rows': rows,
        'per_page': PER_PAGE,
        'page': page,
        'total': total
    })


@app.route('/del')
def delete():
    request_id = request.args.get('request_id')
    if request_id:
        req = Request.query.filter_by(id=request_id).first()
        if req:
            _spidercls = mock_spidercls()
            _spidercls.name = req.spider.name
            _request = request_from_dict(dict(request=req.data), _spidercls)
            storage_name = req.storage.name
            delete_cache(storage_name, _spidercls, _request)

            db.session.delete(req)
            db.session.commit()
    return jsonify(**dict(
        success=True,
        code=0,
        data=[],
        message=''
    ))


if __name__ == '__main__':
    app.run()
