from itsdangerous import URLSafeTimedSerializer
from server import login_manager, app
from server.models import User

login_serializer = URLSafeTimedSerializer(app.secret_key)


@login_manager.token_loader
def get_token_by_id(token):
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()

    # Decrypt the Security Token, data = [username, hashpass]
    data = login_serializer.loads(token, max_age=max_age)

    # Find the User
    user = User.get(data[0])

    # Check Password and return user or None
    if user and data[1] == user.password:
        return user

    return None