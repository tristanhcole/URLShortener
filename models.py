from app import db
from sqlalchemy.ext.declarative import declared_attr


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)


class ShortLink(Base):
    # todo: random id
    slug = db.Column(db.String)
    dest = db.Column(db.String)

    def __repr__(self):
        return f'ShortLink {id}'

