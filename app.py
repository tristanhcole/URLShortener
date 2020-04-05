from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# from models import ShortLink

demo_data = {'asdf': 'http://google.com/'}
current_random_slug_id = 1

BASE62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def decode(string, base=BASE62):
    """
    Decode any string to integer.
    :param string: unique string to decode
    :param base: base to decode from
    :return: original unique  integer
    """
    base_len = len(base)

    num = 0
    for i, c in enumerate(string[::-1]):
        num += (base_len ** i) * base.find(c)
    return num


def encode(num, base=BASE62):
    """
    Encode any integer to any base string. Generates a unique random slug.
    :param num: unique random integer
    :param base: BASE to encode to
    :return: unique random slug
    """
    base_len = len(base)
    if num < base_len:
        return base[num]
    else:
        return encode(num // base_len, base) + base[num % base_len]


def generate_random_slug():
    global current_random_slug_id
    # new_slug = base_conversion(current_random_slug_id)
    # current_random_slug_id += 1
    # return new_slug
    while True:
        slug = encode(current_random_slug_id, BASE62)
        current_random_slug_id += 1
        # TODO(DB): Make sure the slug isn't already used
        existing = DB.get({'slug': slug})
        if not existing:
            return slug



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<string:slug>', methods=['GET'])
def slug(slug):
    demo_dest = demo_data[slug]
    if demo_dest is not None:
        return demo_dest

    return f"Destination not found for {slug}"


@app.route('/api/v1/shortlink', methods=['POST'])
def shortlink():
    data = request.get_json()

    slug = data['slug']
    dest = data['dest']
    if dest:
        if not slug:
            slug = generate_random_slug()

        demo_data[slug] = dest
        # todo: increment random_slug_id

        return 'Added'

    else:
        return 'Must provide destination url'


if __name__ == "__main__":
    app.run()
