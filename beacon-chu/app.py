#!/usr/bin/env python3

from flask import Flask, request, abort
import os

app = Flask(__name__)
# CHU: Cookie Hack Utility


@app.route('/health')
def health():
    return 'hello'


@app.route('/getcookie')
def getcookie():
    if request.headers['Cookie-Secret'] == os.environ.get('COOKIE_SECRET', None):
        return request.cookies.get('access_token')
    else:
        return abort(401)


def main():
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
