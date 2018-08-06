#!usr/bin/env python3.4


from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/api/true")
def mock_true():
    return jsonify({'beacon': 'Always True', 'response': True, 'query': request.args})


@app.route("/api/false")
def mock_false():
    return jsonify({'beacon': 'Always False', 'response': False, 'query': request.args})


@app.route("/api/null")
def mock_null():
    return jsonify({'beacon': 'Always Null', 'response': None, 'query': request.args})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
