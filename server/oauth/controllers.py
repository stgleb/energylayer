import json

import io

from flask import redirect
from flask import request, url_for
from flask import send_file
from flask import session
from flask.ext.login import current_user

from requests_oauthlib import OAuth1Session, OAuth2Session

from server import app
from server.oauth.oauth_config import FACEBOOK_ACCESS_TOKEN_URL
from server.oauth.oauth_config import FACEBOOK_AUTHORIZE_URL
from server.oauth.oauth_config import FACEBOOK_BASE_URL
from server.oauth.oauth_config import FACEBOOK_CONSUMER_KEY
from server.oauth.oauth_config import FACEBOOK_SECRET_KEY
from server.oauth.oauth_config import FACEBOOK_API_VERSION
from server.oauth.oauth_config import TWITTER_ACCESS_TOKEN_URL
from server.oauth.oauth_config import TWITTER_AUTHORIZATION_URL
from server.oauth.oauth_config import TWITTER_BASE_URL
from server.oauth.oauth_config import TWITTER_CONSUMER_KEY
from server.oauth.oauth_config import TWITTER_REQUEST_TOKEN_URL
from server.oauth.oauth_config import TWITTER_SECRET_KEY
from server.oauth.utils import twitter_get_user_details
from server.oauth.utils import twitter_get_or_create_user
from server.oauth.utils import twitter_connect_to_profile


@app.route('/oauth/twitter')
def twitter_access():
    oauth = OAuth1Session(TWITTER_CONSUMER_KEY, client_secret=TWITTER_SECRET_KEY)
    fetch_response = oauth.fetch_request_token(TWITTER_REQUEST_TOKEN_URL)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    authorize_url = TWITTER_AUTHORIZATION_URL + '?oauth_token='
    authorize_url = authorize_url + resource_owner_key

    session['twitter_keys'] = (resource_owner_key, resource_owner_secret)

    return redirect(authorize_url)


@app.route('/callback/twitter')
def twitter_callback():
    verifier = request.args.get('oauth_verifier')
    resource_owner_key, resource_owner_secret = session['twitter_keys']

    twitter = OAuth1Session(TWITTER_CONSUMER_KEY,
                            client_secret=TWITTER_SECRET_KEY,
                            resource_owner_key=resource_owner_key,
                            resource_owner_secret=resource_owner_secret,
                            verifier=verifier)

    oauth_tokens = twitter.fetch_access_token(TWITTER_ACCESS_TOKEN_URL)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    twitter = OAuth1Session(TWITTER_CONSUMER_KEY,
                            client_secret=TWITTER_SECRET_KEY,
                            resource_owner_key=resource_owner_key,
                            resource_owner_secret=resource_owner_secret)

    # If user is not logged in then register via OAuth or login.
    if not current_user:
        details = twitter_get_user_details(twitter)
        user = twitter_get_or_create_user(details=details,
                                          token=session['twitter_keys'])
    else:
        # Attach social account to existing user profile.

    return json.dumps(details)


@app.route('/oauth/facebook')
def facebook_oauth():
    facebook = OAuth2Session(FACEBOOK_CONSUMER_KEY,
                             redirect_uri='http://0.0.0.0:5000' +
                                          url_for('facebook_callback'),
                             scope=['email', 'public_profile']
                             )

    authorization_url, state = facebook.authorization_url(FACEBOOK_AUTHORIZE_URL)

    # State is used to prevent CSRF, keep this for later.
    session['facebook_oauth_state'] = state
    return redirect(authorization_url)


@app.route("/callback/facebook", methods=["GET"])
def facebook_callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    facebook = OAuth2Session(FACEBOOK_CONSUMER_KEY,
                             state=session['facebook_oauth_state'],
                             redirect_uri='http://0.0.0.0:5000' +
                                          url_for('facebook_callback'),
                             scope=['email', 'public_profile', 'user_about_me'])
    token = facebook.fetch_token(FACEBOOK_BASE_URL + FACEBOOK_ACCESS_TOKEN_URL,
                                 client_secret=FACEBOOK_SECRET_KEY,
                                 authorization_response=request.url
                                 )

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['facebook_oauth_token'] = token
    r = facebook.get(FACEBOOK_BASE_URL + '/me')
    user_id = r.json()['id']
    r3 = facebook.get(FACEBOOK_BASE_URL + FACEBOOK_API_VERSION + user_id + '/picture')
    print(r3.content)

    return send_file(io.BytesIO(r3.content),
                     attachment_filename='avatar.png',
                     mimetype='image/png')
    return str(r2.json())
