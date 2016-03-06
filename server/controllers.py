import io

from flask_security import login_required
from flask_login import current_user
from flask_login import logout_user
from flask import request, send_file
from flask import render_template
from flask import url_for
from flask import redirect

from server import app
from server.forms import EditForm
from server.utils import update_user_profile, save_measurement
from server.utils import get_or_create_device


@app.route('/rs/data/post/<device_id>/<data_string>')
def handle_data_from_device(device_id, data_string):
    """
    Receive and decode data from device
    :param device_id device unique identifier
    :param data_string HEX string with format

    0000 1111 2222 3333 4444 5555 6666 7777
    GPIO  V     A    T   -----------------

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

