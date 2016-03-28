from server.persistence.models import User


def get_user_by_id(email):
    user = User.query.filter_by(email=email).first()

    return user


def add_user(user):
    pass


def delete_user_by_id(user_id):
    pass

