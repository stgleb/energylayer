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
                    first_name=form.firstname.data,
                    last_name=form.lastname.data, )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    finally:
        db.session.close()

    return user


def compare_password(user, password):
    return user.password == hash_password(password)

