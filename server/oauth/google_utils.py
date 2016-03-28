import requests

from server.oauth.oauth_config import GOOGLE_BASE_URL
from server.oauth.providers import GOOGLE
from server.persistence.models import SocialProfile
from server.persistence.models import User
from server.persistence.models import db


def google_get_user_details(session):
    user_info_url = GOOGLE_BASE_URL + '/userinfo'
    r = session.get(user_info_url)

    return r.json()


def google_get_or_create_user(details, token):
    id_str = details['id']
    name = details['name']
    screen_name = details['given_name']
    email = details['email']
    first_name, last_name = name.split(' ')
    profile_image_url = details['picture']

    social_profile = SocialProfile.query.filter_by(social_id=id_str).first()

    if social_profile:
        user = social_profile.user

        return False, user

    user = User(email=email,
                password='',
                username=screen_name,
                first_name=first_name,
                last_name=last_name,
                active=True)

    image = requests.get(profile_image_url)
    social_profile = SocialProfile()
    social_profile.social_id = id_str
    social_profile.nickname = screen_name
    social_profile.access_token = str(token)
    user.social_profiles.append(social_profile)
    social_profile.user = user
    social_profile.provider_name = GOOGLE
    social_profile.avatar = image.content

    try:
        db.session.add(user)
        db.session.add(social_profile)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return True, user


def google_connect_to_profile(user, details, token):
    id_str = details['id_str']
    screen_name = details['given_name']
    profile_image_url = details['profile_image_url']
    social_profile = SocialProfile.query.filter_by(social_id=id_str).first()

    if social_profile and social_profile.user_id and \
                    social_profile.user_id == user.id:
        return True

    if social_profile:
        raise Exception("Social profile already in use")

    image = requests.get(profile_image_url)

    try:
        social_profile = SocialProfile()
        social_profile.social_id = id_str
        social_profile.nickname = screen_name
        social_profile.access_token = str(token)
        social_profile.user = user
        social_profile.avatar = image.content
        social_profile.provider_name = GOOGLE
        user.social_profiles.append(social_profile)

        db.session.add(user)
        db.session.add(social_profile)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

    return True
