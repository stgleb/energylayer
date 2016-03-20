import json
import requests

from server.oauth import TWITTER_BASE_URL
from server.models import User
from server.models import SocialProfile
from server.models import db


def twitter_get_user_details(session):
    user_info_url = TWITTER_BASE_URL + '/account/settings.json'
    r = session.get(user_info_url)
    user_info = json.loads(r.content)
    screen_name = user_info['screen_name']
    user_details_url = TWITTER_BASE_URL + \
                       '/users/show.json?screen_name={0}'. \
                           format(screen_name)
    r = session.get(user_details_url)
    details = json.loads(r.content)

    return details


def twitter_get_or_create_user(details, token):
    id_str = details['id_str']
    name = details['name']
    screen_name = details['screen_name']
    first_name, last_name = name.split(' ')
    profile_image_url = details['profile_image_url']

    social_profile = SocialProfile.query.filter_by(social_id=id_str).first()

    if social_profile:
        user = social_profile.user

        return user

    user = User(email="",
                first_name=first_name,
                last_name=last_name,
                active=True)
    image = requests.get(profile_image_url)
    social_profile = SocialProfile()
    social_profile.social_id = id_str
    social_profile.nickname = screen_name
    social_profile.access_token = token
    user.social_profiles.append(social_profile)
    social_profile.user = user
    social_profile.avatar = image.content

    try:
        db.session.add(user)
        db.session.add(social_profile)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return user


def twitter_connect_to_profile(user, details, token):
    id_str = details['id_str']
    screen_name = details['screen_name']
    profile_image_url = details['profile_image_url']

    image = requests.get(profile_image_url)

    social_profile = SocialProfile()
    social_profile.social_id = id_str
    social_profile.nickname = screen_name
    social_profile.access_token = token
    social_profile.user = user
    social_profile.avatar = image.content
    user.social_profiles.append(social_profile)

    try:
        db.session.add(user)
        db.session.add(social_profile)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

    return True
