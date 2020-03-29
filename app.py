from flask import Flask, request
import random
app = Flask(__name__)

# todo: setup DB
demo_data = {'asdf': 'http://google.com/'}


def generate_random_slug():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    num_chars = 7
    return ''.join([random.choice(alphabet) for _ in range(num_chars)])


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

        return 'Added'

    else:
        return 'Must provide destination url'


if __name__ == "__main__":
    app.run()
