import json

import io

from flask_security import login_required
from flask_login import current_user
from flask_login import logout_user
from flask import request, send_file, Response, send_from_directory
from flask import render_template
from flask import url_for
from flask import redirect

from server import app, security
from server.forms import EditForm
from server.utils import update_user_profile
from server.utils import save_measurement
from server.utils import get_measurements_from_device
from server.utils import get_devices_per_user
from server.utils import get_user_list
from server.utils import attach_device_to_user as attach_device
from server.utils import get_or_create_device


@app.route('/rs/data/post/<device_id>/<data_string>')
def handle_data_from_device(device_id, data_string):
    """
    Receive and decode data from device
    :param device_id device unique identifier
    :param data_string HEX string with format

    0000 1111 2222 3333 4444 5555 6666 7777
    GPIO  V    A    T  Reserved for another sensors

    V - Voltage
    A - Power
    T - Temperature
    """
    ip_addr = request.remote_addr
    device = get_or_create_device(device_id=device_id,
                                  device_ip=ip_addr)

    gpio = int(data_string[:4], 16)
    voltage = int(data_string[4:8], 16)
    power = int(data_string[8:12], 16)
    temperature = int(data_string[12:16], 16)

    save_measurement(device=device,
                     gpio=gpio,
                     voltage=voltage,
                     power=power,
                     temperature=temperature)

    return 'Created', 201


@app.route('/api/measurement/<device_uuid>/', methods=['GET'])
@app.route('/api/measurement/<device_uuid>/<timestamp>', methods=['GET'])
def get_measurements(device_uuid, timestamp=0):
    """
    Get device measurements from given timestamp
    :param device_uuid
    :param timestamp time since measurements
    should be given.
    :return json list [
        {
            "voltage": 220,
            "power": 20,
            "temperature": 22,
            "gpio", 10,
            "timestamp": 1234567
        }
    ]:
    """
    measurements = get_measurements_from_device(device_id=device_uuid,
                                                since=timestamp)

    response = Response(response=json.dumps(measurements),
                        status=200,
                        mimetype="application/json")

    return response


@app.route('/api/<user_id>/device', methods=['GET'])
def get_devices_list(user_id):
    """
    Get list of user's devices
    :return:
    """
    devices = get_devices_per_user(user_id)
    response = Response(response=json.dumps(devices),
                        status=200,
                        mimetype="application/json")

    return response


@app.route('/api/user', methods=['GET'])
def get_users():
    """
    Gives list of users in the system
    :return:
    """
    users = get_user_list()

    response = Response(response=json.dumps(users),
                        status=200,
                        mimetype='application/json')

    return response


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
    attach_device(user_id=user_id, device_id=device_uuid)

    return 'Device added', 200


@app.route('/', methods=['GET'])
@login_required
def index():
    """
    Home page
    :return:
    """
    return render_template('_index.html')


@app.route('/home', methods=['GET'])
def index2():
    """
    Home page
    :return:
    """
    return render_template('_index.html')


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditForm()

    if request.method == 'POST':
        if form.validate():
            image_data = request.files.get('avatar')
            update_user_profile(form, current_user.id,
                                image_data=image_data)
            return redirect(url_for('index'))
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
    if current_user.avatar_image:
        avatar = current_user.avatar_image
    elif current_user.social_profiles:
        avatars = [p.avatar for p in current_user.social_profiles if p.avatar]

        if avatars:
            avatar = avatars[0]
        else:
            avatar = ''
    else:
        avatar = ''

    return send_file(io.BytesIO(avatar),
                     attachment_filename='avatar.png',
                     mimetype='image/png')


@app.route('/static/<path>', methods=['GET'])
def static_content(path):
    return send_from_directory(app.static_folder, path)
