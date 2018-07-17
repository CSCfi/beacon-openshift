#!/usr/bin/env python3
from flask import Flask, abort, request, make_response, session
from uuid import uuid4
import os
import logging
import requests
import requests.auth
import urllib.parse
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']
COOKIE_AGE = os.environ['COOKIE_AGE']
COOKIE_SECURE = os.environ['COOKIE_SECURE']

# Logging
FORMAT = '[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

def user_agent():
    return "what should I return here?"

def base_headers():
    return {"User-Agent": user_agent()}


app = Flask(__name__)

@app.route('/app')
def homepage():
    text = '<a href="%s">Authenticate with elixir</a>'
    return text % make_authorization_url()


def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "temporary",
              "scope": 'openid bona_fide_status'}
    url = "https://login.elixir-czech.org/oidc/authorize?" + urllib.parse.urlencode(params)
    return url


# You may want to store valid states in a database or memcache.
# But that is beyond this small test
def save_created_state(state):
    pass
def is_valid_state(state):
    return True

@app.route('/')
def elixir_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    # Note: In most cases, you'll want to store the access token, in, say,
    # a session for use in other parts of your web app.
    userdetails = get_userdetails(access_token)
    #cookie = set_cookie(access_token)
    response = app.make_response(userdetails)
    response.set_cookie('access_token', access_token, max_age=COOKIE_AGE, secure=COOKIE_SECURE)  # domain=ip
    return response


@app.route('/set_cookie')
def set_cookie():
    access_token = 'test'
    LOG.info('SET COOKIE: ' + access_token)
    res = make_response('Set cookie')
    #res.set_cookie('access_token', access_token, max_age=30, secure=True)  # HTTPS only
    res.set_cookie('access_token', access_token, max_age=COOKIE_AGE, secure=COOKIE_SECURE)
    return res

@app.route('/get_cookie')
def get_cookie():
    cookie = request.cookies.get('access_token')
    return cookie

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://login.elixir-czech.org/oidc/token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json['access_token']


def get_userdetails(access_token):
    headers = base_headers()
    headers.update({"Authorization": "Bearer " + access_token})
    response = requests.get("https://login.elixir-czech.org/oidc/userinfo",
                            headers=headers)
    userdetails = response.json()
    return userdetails['sub']


def main():
    app.secret_key = os.environ['COOKIE_SECRET']
    #app.config['SESSION_COOKIE_SECURE'] = True
    host = os.environ['APP_HOST']
    port = os.environ['APP_PORT']
    debug = os.environ['APP_DEBUG']
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
