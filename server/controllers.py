from flask.ext.login import login_required
from flask_login import login_user, current_user
from flask_login import logout_user
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect

from server import app, login_manager
from server.forms import LoginForm, SignupForm, EditForm
from server.models import User
from server.persistence.token import login_serializer
from server.utils import register_user, get_user_by_id, update_user_profile


@app.route('/api/measurement/<device_uuid>', methods=['POST'])
def receive_measurements(device_uuid):
    """
    Accept measurement data from device
    :param device_uuid:
    :return:
    """
    raise NotImplementedError()


@app.route('/api/measurement/<device_uuid>/<time_stamp>', methods=['GET'])
def send_measurement(device_uuid, time_stamp=0):
    """
    Send device measurements from given timestamp
    :param device_uuid:
    :return:
    """
    raise NotImplementedError()


@app.route('/api/<user_id>/device', methods=['GET'])
def get_devices_list(user_id):
    """
    Get list of user's devices
    :return:
    """
    raise NotImplementedError()


@app.route('/api/user', methods=['GET'])
def get_users():
    """
    Gives list of users in the system
    :return:
    """
    raise NotImplementedError()


@app.route('/api/user/<user_id>', methods=['GET'])
def get_user_details(user_id):
    """
    Get details of particular user
    :param user_id:
    :return:
    """
    raise NotImplementedError()


@app.route('/api/user/<user_id>/<device_uuid>', methods=['PATCH'])
def attach_device_to_user(user_id, device_uuid):
    raise NotImplementedError()


@app.route('/', methods=['GET'])
@login_required
def index():
    """
    Home page
    :return:
    """
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('login'))


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditForm()

    if request.method == 'POST':
        if form.validate():
            update_user_profile(form, current_user.id)
            return render_template('index.html')
        else:
            return render_template('edit.html', form=form)
    else:
        return render_template('edit.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
@login_manager.unauthorized_handler
def login():
    """
    Login user
    :return:
    """
    form = LoginForm()

    if request.method == 'POST':
        if form.validate():
            if login_user(form.user, remember=True):
                return redirect(url_for('index'))

    return render_template('login.html', login_form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register new user in system.
    :return:
    """
    form = SignupForm()

    if request.method == 'POST':
        if form.validate():
            user = register_user(form)

            if login_user(user, remember=True):
                return redirect(url_for('index'))

    return render_template('login.html', register_form=form)


@login_manager.user_loader
def _load_user(user_id):
    user = get_user_by_id(user_id)

    return user


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


# @login_manager.request_loader
# def load_user(request):
#     token = request.headers.get('Authorization')
#
#     if token is None:
#         token = request.args.get('token')
#
#     if token is not None:
#         username, password = token.split(":")  # naive token
#         user_entry = User.get(username)
#         if user_entry is not None:
#             user = User(user_entry[0], user_entry[1])
#             if user.password == password:
#                 return user
#     return None
