import io

from flask_security import login_required
from flask_login import current_user
from flask_login import logout_user
from flask import request, send_file, send_from_directory
from flask import render_template
from flask import url_for
from flask import redirect

from server import app
from server.config import PER_PAGE, METRICS, UNITS, TOTAL_COUNT
from server.forms import EditForm
from server.pagination import Pagination
from server.utils import attach_device_to_user, get_measurement_value, get_ip_coordinates, ceil_power, fill_with_random
from server.utils import get_measurements_by_count
from server.utils import get_all_measurements_count
from server.utils import dettach_device_from_user
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


@app.route('/dashboard/<metric>', methods=['GET'])
@app.route('/dashboard', methods=['GET'])
# @login_required
def dashboard(metric="voltage"):
    """
    Controller for dashboard page.

    :param metric: metric type 'voltage', 'power' 'temperature'
    :return:
    """
    devices = []

    # Get list of user devices
    if current_user.is_authenticated:
        devices = [device.uuid for device in current_user.devices.all()]
    else:
        devices.extend([device['uuid'] for device in get_all_devices()])

    initial_measurements = {}
    y_maximums = []

    for device_id in devices:
        measurements = get_measurements_by_count(device_id, TOTAL_COUNT, 1)[::-1]
        tmp = [[0, get_measurement_value(m, metric=metric)] for m in measurements]

        if tmp:
            y_max = max([t[1] for t in tmp])
        else:
            y_max = 0

        y_max = ceil_power(y_max, 10)
        y_maximums.append(y_max)

        initial_measurements[device_id] = tmp

    return render_template('chart.html',
                           devices=devices,
                           devices_count=len(devices),
                           metric_to_display=metric,
                           metrics=METRICS,
                           unit=UNITS[metric],
                           measurements=initial_measurements,
                           maximums=y_maximums)


@app.route('/dashboard/device/<device_id>', methods=['GET'])
def device_chart(device_id=None):
    """
    Dashboard page

    :param device_id: Device UUID
    :return:
    """
    max_values = []
    initial_measurements = get_measurements_by_count(device_id, 180, 1)
    initial_measurements = initial_measurements[::-1]

    for metric in METRICS:
        max_value = max([m[metric] for m in initial_measurements])
        max_value = ceil_power(max_value, 10)
        max_values.append(max_value)

    # Get list of user devices
    if current_user.is_authenticated:
        devices_all = current_user.devices.all()
        devices = [device.uuid for device in devices_all]
        other_devices = [device.uuid for device in devices_all]

        if device_id:
            devices = [device for device in devices if device == device_id]
    else:
        devices_all = [device['uuid'] for device in get_all_devices()]
        other_devices = [device for device in devices_all]
        devices = [device for device in devices_all
                   if device == device_id]

    return render_template('device_chart.html',
                           metrics=METRICS,
                           devices=devices,
                           devices_count=len(devices),
                           other_devices=other_devices,
                           measurements=initial_measurements,
                           max_values=max_values)


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
        devices = get_all_devices()

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


@login_required
@app.route('/api/user/device/<device_id>/detach', methods=['GET'])
def dettach_device(device_id=None):
    """
    Dettach device to particular user, has user:device has
    1:many relation. Params in form.

    :return:
    """
    user_id = current_user.id
    devices = get_devices_per_user(user_id=user_id)

    try:
        dettach_device_from_user(user_id=user_id, device_id=device_id)
    except Exception as e:
        return render_template('devices.html', devices=devices,
                               error=str(e))

    return redirect(url_for('user_devices'))


@app.route("/device/<device_id>/table")
@app.route("/device/<device_id>/table/<int:page>")
def get_table_for_device(device_id, page=1):
    count = get_all_measurements_count(device_id=device_id)

    measurements = get_measurements_by_count(device_id=device_id,
                                             count=PER_PAGE,
                                             offset=page)

    pagination = Pagination(page, PER_PAGE, count)

    return render_template('table.html',
                           pagination=pagination,
                           measurements=measurements,
                           page=page,
                           PER_PAGE=PER_PAGE
                           )


@app.route("/user/maps")
def user_maps():
    if current_user.is_authenticated:
        devices = get_devices_per_user(current_user.id)
    else:
        devices = get_all_devices()

    coordinates = [(get_ip_coordinates(device['ip_addr'])[0],
                   get_ip_coordinates(device['ip_addr'])[1],
                   device['uuid']) for device in devices if device['ip_addr']]

    center = (50.0, 35.0)

    return render_template("maps.html",
                           coordinates=coordinates,
                           center=center)


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
