from flask import redirect
from flask import request, url_for
from flask import session
from flask.ext.login import current_user
from flask.ext.login import login_required
from flask_login import login_user
from requests_oauthlib import OAuth1Session, OAuth2Session

from server import app
from server import db

from server.oauth.oauth_config import FACEBOOK_ACCESS_TOKEN_URL
from server.oauth.oauth_config import FACEBOOK_AUTHORIZE_URL
from server.oauth.oauth_config import FACEBOOK_BASE_URL
from server.oauth.oauth_config import FACEBOOK_CONSUMER_KEY
from server.oauth.oauth_config import FACEBOOK_SECRET_KEY
from server.oauth.oauth_config import TWITTER_ACCESS_TOKEN_URL
from server.oauth.oauth_config import TWITTER_AUTHORIZATION_URL
from server.oauth.oauth_config import TWITTER_CONSUMER_KEY
from server.oauth.oauth_config import TWITTER_REQUEST_TOKEN_URL
from server.oauth.oauth_config import TWITTER_SECRET_KEY

from server.oauth.twitter_utils import twitter_get_user_details
from server.oauth.twitter_utils import twitter_get_or_create_user
from server.oauth.twitter_utils import twitter_connect_to_profile

from server.oauth.facebook_utils import facebook_get_user_details
from server.oauth.facebook_utils import facebook_get_or_create_user
from server.oauth.facebook_utils import facebook_connect_to_profile


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
    details = twitter_get_user_details(twitter)
    # If user is not logged in then register via OAuth or login.
    if current_user.is_anonymous:
        _, user = twitter_get_or_create_user(details=details,
                                             token=session['twitter_keys'])
        login_user(user)
    else:
        try:
            # Attach social account to existing user profile.
            twitter_connect_to_profile(current_user, details,
                                       (resource_owner_key,
                                        resource_owner_secret))
        except Exception as e:
            redirect(url_for('profile'),
                     oauth_error='Profile is already in use')

    return redirect(url_for('index'))


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
    facebook = OAuth2Session(FACEBOOK_CONSUMER_KEY,
                             state=session['facebook_oauth_state'],
                             redirect_uri='http://0.0.0.0:5000' +
                                          url_for('facebook_callback'),
                             scope=['email', 'public_profile', 'user_about_me'])
    token = facebook.fetch_token(FACEBOOK_BASE_URL + FACEBOOK_ACCESS_TOKEN_URL,
                                 client_secret=FACEBOOK_SECRET_KEY,
                                 authorization_response=request.url
                                 )
    session['facebook_oauth_token'] = token
    details = facebook_get_user_details(facebook)

    if current_user.is_anonymous:
        _, user = facebook_get_or_create_user(details=details,
                                              token=token)
        login_user(user, True)
    else:
        try:
            facebook_connect_to_profile(current_user,
                                        details=details,
                                        token=token)
        except Exception as e:
            redirect(url_for('profile'),
                     oauth_error='Profile is already in use')

    return redirect(url_for('index'))


@app.route('/disconnect/<provider_name>')
@login_required
def disconnect(provider_name):
    profiles = current_user.social_profiles
    profile = [p for p in profiles if p.provider_name == provider_name]

    try:
        if profile:
            current_user.social_profiles.remove(profile[0])
            db.session.commit()
    except Exception as e:
        db.session.rollback()

    return redirect(url_for('edit_user'))
