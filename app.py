from flask import Flask, request, redirect, make_response, jsonify
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

            response_object = dict(slug=str(link.slug), dest=str(link.dest))
            return response_object, 200

        except (IntegrityError, InvalidSlug, InvalidDest) as e:
            if isinstance(e, InvalidSlug) or isinstance(e, InvalidDest):
                response_object = dict(message=str(e))
                return response_object, 400

            from psycopg2 import errors
            db.session.rollback()

            if isinstance(e.orig, errors.UniqueViolation) and slug:
                response_object = dict(message='Slug already exists')
                return response_object, 409
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
        return redirect(link.dest)

    return f"Destination not found for {slug}"


@app.route('/api/v1/shortlink', methods=['POST'])
def shortlink():
    data = request.get_json()

    slug = data.get('slug')
    dest = data.get('dest')

    response_object, status_code = generate_shortlink(slug=slug, dest=dest)

    if status_code == 200:
        db.session.commit()

    return make_response(jsonify(response_object)), status_code


if __name__ == "__main__":
    app.run()
