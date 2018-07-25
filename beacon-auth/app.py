#!/usr/bin/env python3

from flask import Flask, abort, request, make_response, session, redirect
from uuid import uuid4
import os
import logging
import requests
import requests.auth
import urllib.parse


CLIENT_ID = os.environ.get('CLIENT_ID', None)
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', None)
REDIRECT_URI = os.environ.get('REDIRECT_URI', None)

# Logging
FORMAT = '[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def user_agent():
    return "ELIXIR Beacon Login"


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
    LOG.info('callback 1')
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
    #userdetails = get_userdetails(access_token)  # DISABLED FOR NOW
    #response = app.make_response(userdetails)
    LOG.info('callback 2')
    try:
        response = app.make_response(redirect(os.environ.get('COOKIE_DOMAIN', None))
        response.set_cookie('access_token',
                            access_token,
                            max_age=os.environ.get('COOKIE_AGE', 3600),
                            secure=os.environ.get('COOKIE_SECURE', True),
                            domain=os.environ.get('COOKIE_DOMAIN', None))
        LOG.info('cookie is set')
    except Exception as e:
        LOG.error(str(e))
    return response


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

''' DISABLED FOR TESTING
def get_userdetails(access_token):
    headers = base_headers()
    headers.update({"Authorization": "Bearer " + access_token})
    response = requests.get("https://login.elixir-czech.org/oidc/userinfo",
                            headers=headers)
    userdetails = response.json()
    return userdetails['sub']
'''

def main():
    app.secret_key = os.environ.get('COOKIE_SECRET', None)
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', True)
    app.run(host=os.environ.get('APP_HOST', 'localhost'),
            port=os.environ.get('APP_PORT', 8080),
            debug=os.environ.get('APP_DEBUG', True))


if __name__ == '__main__':
    main()
