import os

from server.oauth.oauth_config import FACEBOOK_BASE_URL
from server.models import User
from server.models import SocialProfile
from server.models import db
from server.oauth.providers import FACEBOOK


def facebook_get_user_details(session):
    r = session.get(FACEBOOK_BASE_URL + '/me')
    data = r.json()
    user_id = data['id']
    first_name, last_name = data['name'].split(' ')
    picture = session.get(FACEBOOK_BASE_URL + '/v2.5/' + user_id + '/picture')

    details = dict()
    details['picture'] = picture.content
    details['id'] = user_id
    details['first_name'] = first_name
    details['last_name'] = last_name
    details['name'] = data['name']

    return details


def facebook_get_or_create_user(details, token):
    user_id = details['id']
    nickname = details['name']
    first_name = details['first_name']
    last_name = details['last_name']
    picture = details['picture']

    social_profile = SocialProfile.query.filter_by(social_id=user_id).first()

    if social_profile:
        user = social_profile.user

        return False, user

    user = User(email=os.urandom(12),
                password='',
                first_name=first_name,
                last_name=last_name,
                active=True)

    social_profile = SocialProfile()
    social_profile.social_id = user_id
    social_profile.nickname = nickname
    social_profile.access_token = str(token)
    user.social_profiles.append(social_profile)
    social_profile.user = user
    social_profile.provider_name = FACEBOOK
    social_profile.avatar = picture

    try:
        db.session.add(user)
        db.session.add(social_profile)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return True, user


def facebook_connect_to_profile(user, details, token):
    user_id = details['id']
    nickname = details['name']
    picture = details['picture']

    social_profile = SocialProfile.query.filter_by(social_id=user_id).first()

    if social_profile and social_profile.user_id and social_profile.user_id == user.id:
        return True

    if social_profile:
        raise Exception("Social profile already in use")

    try:
        social_profile = SocialProfile()
        social_profile.social_id = user_id
        social_profile.nickname = nickname
        social_profile.access_token = str(token)
        social_profile.avatar = picture
        social_profile.user = user
        social_profile.provider_name = FACEBOOK
        user.social_profiles.append(social_profile)

        db.session.add(user)
        db.session.add(social_profile)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

    return True
