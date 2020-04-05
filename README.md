# URLShortener
![GitHub](https://img.shields.io/github/license/tristanhcole/URLShortener)

Python URL Shortener

Todo:
- React front end
- Handle unusual, but valid path characters .+!*()_$-
- backend tests

### Setup
- Install python requirements
``pip install -r requirements.txt``

- Create database
``urlshortener``

- Run migrations
``python manage.py db upgrade``

### How it works
##### [POST] Creating a new shortlink
``http://127.0.0.1:5000/api/v1/shortlink``

Body:
``{ "dest": "http://example.com"}``

Optional: Provide a custom slug

##### [GET] Redirection
GET ``http://127.0.0.1:5000/$SLUG``

Returns a 302 redirection.

### Design
The URL Shortener uses the next `shortlink_id_seq` to convert into a random, unique, URL friendly slug via a base encoder.
This ensures that the links are fast to create, unique, short and we can store a large amount.

Currently a 62 alphabet is used, meaning with a 7 character slug there are ~5 trillion unique combinations.

Built with Flask and Python