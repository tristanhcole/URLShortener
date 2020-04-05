import datetime
from app import db
from utils import encode, decode
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import Sequence


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class ShortLink(Base):
    slug = db.Column(db.String, unique=True, index=True, nullable=False)
    dest = db.Column(db.String)

    def __init__(self, **kwargs):
        if kwargs.get('slug') is None:
            current_random_slug_id = db.session.execute(Sequence("shortlink_id_seq"))
            kwargs['id'] = current_random_slug_id
            kwargs['slug'] = encode(current_random_slug_id)
        else:
            kwargs['id'] = decode(kwargs['slug'])

        super(ShortLink, self).__init__(**kwargs)

    def __repr__(self):
        return f'ShortLink {id}'

