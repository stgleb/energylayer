import hashlib
from flask.ext.login import current_user
from server.models import db, User


def hash_password(password):
    encoded = password.encode('utf-8')
    return hashlib.md5(encoded).hexdigest()


def register_user(form):
    user = None

    try:
        password_hash = hash_password(form.password.data)

        user = User(email=form.email.data,
                    password=password_hash,
                    username=form.username.data,
                    first_name=form.firstname.data,
                    last_name=form.lastname.data)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    finally:
            db.session.close()

    return user


def compare_password(user, password):
    return user.password == hash_password(password)


def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()

    return user


def update_user_profile(form, user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        user.email = form.email.data
        user.first_name = form.firstname.data
        user.last_name = form.lastname.data
        user.username = form.username.data
        user.email = form.email.data
        password_hash = hash_password(form.password.data)
        user.password = password_hash
        db.session.commit()
    except Exception as e:
        db.session.rollback()
