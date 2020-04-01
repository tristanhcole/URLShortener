from flask import Flask, request
import random
app = Flask(__name__)

# todo: setup DynamoDB
demo_data = {'asdf': 'http://google.com/'}
DB = None
current_random_slug_id = 1

# model
# shortlink
#   - slug (/asdf)
#   - dest (google.com)


# todo: decode str, to int

# todo(rename): encode number, return str

BASE62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def base_conversion(n, base=BASE62):
    """
    Convert integer to base62 slug to generate unique random slug
    :param n:
    :param base:
    :return:
    """
    alphabet = BASE62
    if n < base:
        return alphabet[n]
    else:
        return base_conversion(n//base, base) + alphabet[n%base]


def generate_random_slug():
    global current_random_slug_id
    # new_slug = base_conversion(current_random_slug_id)
    # current_random_slug_id += 1
    # return new_slug
    while True:
        slug = base_conversion(current_random_slug_id, BASE62)
        current_random_slug_id += 1
        # Make sure the slug isn't already used
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
