#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)
# CHU: Cookie Hack Utility


@app.route('/health')
def health():
    return 'hello'


@app.route('/getcookie')
def getcookie():
    cookie = request.cookies.get('access_token')
    return cookie


def main():
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
