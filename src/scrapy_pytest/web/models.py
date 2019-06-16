from .exts import db

__all__ = ['db', 'Storage', 'Spider', 'ParseFunc', 'Request']


class Storage(db.Model):
    __tablename__ = 'storage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


class Spider(db.Model):
    __tablename__ = 'spider'

    id = db.Column(db.Integer, primary_key=True)
    storage_id = db.Column(db.Integer, db.ForeignKey('storage.id'))
    name = db.Column(db.String(40), nullable=False)

    storage = db.relationship('Storage', backref='spider')


class ParseFunc(db.Model):
    __tablename__ = 'parse_func'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    spider_id = db.Column(db.Integer, db.ForeignKey('spider.id'))

    spider = db.relationship('Spider', backref='parse_func')


class Request(db.Model):
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    parse_func_id = db.Column(db.Integer, db.ForeignKey('parse_func.id'))
    data = db.Column(db.Binary, nullable=False)

    parse_func = db.relationship('ParseFunc', backref='request')
