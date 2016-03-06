import io

from flask_security import login_required
from flask_login import login_user, current_user
from flask_login import logout_user
from flask import request, send_file
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
            image_data = request.files.get('avatar')
            update_user_profile(form, current_user.id,
                                image_data=image_data)
            return render_template('index.html')
        else:
            return render_template('edit.html', form=form)
    else:
        return render_template('edit.html', form=form)


@app.route('/avatar', methods=['GET'])
@login_required
def get_avatar():
    """
    Gets avatar image from database.
    :return:
    """
    avatar = current_user.avatar_image
    return send_file(io.BytesIO(avatar),
                     attachment_filename='avatar.png',
                     mimetype='image/png')

