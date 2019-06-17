from .exts import db

__all__ = ['db', 'Storage', 'Spider', 'ParseFunc', 'Request']


class Storage(db.Model):
    __tablename__ = 'storage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Storage(id=%s, name=%s)>' % (self.id, self.name)


class Spider(db.Model):
    __tablename__ = 'spider'

    id = db.Column(db.Integer, primary_key=True)
    storage_id = db.Column(db.Integer, db.ForeignKey('storage.id'))
    name = db.Column(db.String(40), nullable=False)

    storage = db.relationship('Storage', backref='spider')

    def __repr__(self):
        return '<Spider(id=%s, name=%s, storage_id=%s)>' % (self.id, self.name, self.storage_id)


class ParseFunc(db.Model):
    __tablename__ = 'parse_func'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    spider_id = db.Column(db.Integer, db.ForeignKey('spider.id'))

    spider = db.relationship('Spider', backref='parse_func')

    def __repr__(self):
        return '<ParseFunc(id=%s, name=%s, spider_id=%s)>' % (self.id, self.name, self.spider_id)


class Request(db.Model):
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    parse_func_id = db.Column(db.Integer, db.ForeignKey('parse_func.id'))
    storage_id = db.Column(db.Integer, db.ForeignKey('storage.id'))
    spider_id = db.Column(db.Integer, db.ForeignKey('spider.id'))
    data = db.Column(db.Binary, nullable=False)

    parse_func = db.relationship('ParseFunc', backref='request')
    spider = db.relationship('Spider', backref='request')
    storage = db.relationship('Storage', backref='request')

    def __repr__(self):
        return '<Request(id=%s, name=%s, parse_func_id=%s, spider=%s, storage=%s)>' % (
            self.id, self.name, self.parse_func_id, self.spider.name, self.storage.name)
