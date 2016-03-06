import hashlib
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

    return user


def compare_password(user, password):
    return user.password == hash_password(password)


def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()

    return user


def update_user_profile(form, user_id, image_data=None):
    try:
        user = User.query.filter_by(id=user_id).first()

        if form.email.data:
            user.email = form.email.data

        if form.firstname.data:
            user.first_name = form.firstname.data

        if form.lastname.data:
            user.last_name = form.lastname.data

        if form.username.data:
            user.username = form.username.data

        if form.email.data:
            user.email = form.email.data

        if image_data:
            user.avatar_image = image_data.stream.read()

        db.session.commit()
    except Exception as e:
        db.session.rollback()
