from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
import pickle

from .config import DevelopmentConfig
from .common import save_data
from .exts import db
from .models import Request

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()


@app.template_filter('loads_url')
def loads_meta(value):
    dat = pickle.loads(value)
    return dat['url']


@app.template_filter('loads_meta')
def loads_meta(value):
    dat = pickle.loads(value)
    return dat['meta']


@app.route('/')
def home():
    PER_PAGE = 15
    save_data()
    page = request.args.get(get_page_parameter(), default=1, type=int)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    total = len(Request.query.all())
    pagination = Pagination(bs_version=3, page=page, total=total)
    reqs = Request.query.slice(start, end)
    return render_template('index.html', **{'reqs': reqs, 'pagination': pagination})


@app.route('/del/<request_id>')
def delete(request_id):
    req = Request.query.filter_by(id=request_id).fisrt()
    db.session.delete(req)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
