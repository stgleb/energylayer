import io

from flask_security import login_required
from flask_login import current_user
from flask_login import logout_user
from flask import request, send_file, send_from_directory
from flask import render_template
from flask import url_for
from flask import redirect

from server import app
from server.forms import EditForm
from server.utils import attach_device_to_user
from server.utils import get_devices_per_user
from server.utils import get_all_devices
from server.utils import update_user_profile


@app.route('/', methods=['GET'])
# @login_required
def index():
    """
    Home page
    :return:
    """
    return render_template('_index.html')


# Old version of Dashboard
@app.route('/dashboard/old', methods=['GET'])
@login_required
def dashboard_old():
    """
    Dashboard page
    :return:
    """
    return render_template('dashboard_pages/dashboard.html')


@app.route('/dashboard', methods=['GET'])
# @login_required
def dashboard(device_id=None):
    """
    Dashboard page
    :return:
    """
    devices = []

    # Get list of user devices
    if current_user.is_authenticated:
        devices = [device.uuid for device in current_user.devices.all()]
    else:
        devices.append("Your_future_device")

    return render_template('chart.html', devices=devices,
                           devices_count=len(devices))


@app.route('/dashboard/<device_id>', methods=['GET'])
def device_chart(device_id=None):
    """
    Dashboard page
    :return:
    """
    devices = []

    # Get list of user devices
    if current_user.is_authenticated:
        devices = [device.uuid for device in current_user.devices.all()]

        if device_id:
            devices = [device for device in devices if device == device_id]
    else:
        devices = get_all_devices()[:1]

    return render_template('device_chart.html',
                           metrics=["voltage", "power", "temperature"],
                           devices=devices,
                           devices_count=len(devices))


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


@app.route('/user/devices')
# @login_required
def user_devices(device_id=None):
    devices = []

    if current_user.is_authenticated:
        devices = get_devices_per_user(current_user.id)

    else:
        devices = []

    return render_template('devices.html', devices=devices)


@app.route('/edit', methods=['GET', 'POST'])
# @login_required
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


@login_required
@app.route('/api/user', methods=['POST'])
def attach_device():
    """
    Attach device to particular user, has user:device has
    1:many relation. Params in form.

    :return:
    """
    user_id = current_user.id
    devices = get_devices_per_user(user_id=user_id)
    device_uuid = request.form['device_uuid']

    try:
        attach_device_to_user(user_id=user_id, device_id=device_uuid)
    except Exception as e:
        return render_template('devices.html', devices=devices,
                               error="Device is already used")

    return redirect(url_for('user_devices'))


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
