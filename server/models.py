import datetime, os
from server.app import db
from server.utils import encode, decode, validate_dest, validate_slug
from server.exceptions import InvalidDest, InvalidSlug
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import Sequence


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.BigInteger, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class ShortLink(Base):
    _slug = db.Column(db.String, unique=True, index=True, nullable=False)
    _dest = db.Column(db.String, nullable=False)

    @hybrid_property
    def link(self):
        return os.environ['HOST'] + self.slug

    @hybrid_property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, val):
        try:
            self._slug = validate_slug(val)
        except InvalidSlug as e:
            raise e

    @hybrid_property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, val):
        try:
            self._dest = validate_dest(val)
        except InvalidDest as e:
            raise e

    def __init__(self, **kwargs):
        # First, validate user inputs
        self.slug = kwargs.get('slug')
        self.dest = kwargs.get('dest')

        # Next, generate unique slug OR unique id
        if kwargs.get('slug') is None:
            current_random_slug_id = db.session.execute(Sequence("shortlink_id_seq"))
            kwargs['id'] = current_random_slug_id
            kwargs['slug'] = encode(current_random_slug_id)
        else:
            kwargs['id'] = decode(kwargs['slug'])

        super(ShortLink, self).__init__(**kwargs)

    def __repr__(self):
        return f'ShortLink {id}'

