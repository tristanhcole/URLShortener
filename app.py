from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


def generate_shortlink(slug, dest):
    while True:
        try:
            link = ShortLink(
                dest=dest,
                slug=slug
            )
            db.session.add(link)
            db.session.flush()

            response = {'slug': link.slug, 'dest': link.dest}
            return response, 200

        except IntegrityError as e:
            from psycopg2 import errors
            db.session.rollback()
            if isinstance(e.orig, errors.UniqueViolation) and slug:
                return 'Slug already exists', 409
            pass


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<string:slug>', methods=['GET'])
def slug(slug):
    if slug is None:
        return 'Slug cannot be None'

    link = db.session.query(ShortLink).filter_by(slug=slug).first()
    if link is not None:
        return link.dest

    return f"Destination not found for {slug}"


@app.route('/api/v1/shortlink', methods=['POST'])
def shortlink():
    data = request.get_json()

    slug = data.get('slug')
    dest = data.get('dest')
    if dest:
        response, status_code = generate_shortlink(slug=slug, dest=dest)

        if status_code == 200:
            db.session.commit()

        return response, status_code

    else:
        return 'Must provide destination url'


if __name__ == "__main__":
    app.run()
