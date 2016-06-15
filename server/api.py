import json

from flask import Response
from flask import request
from flask.ext.login import current_user

from server import app
from server.config import TOTAL_COUNT
from server.utils import get_or_create_device
from server.utils import get_measurements_by_count_for_devices
from server.utils import get_all_devices
from server.utils import get_measurements_by_timestamp
from server.utils import get_measurements_by_count
from server.utils import get_devices_per_user
from server.utils import get_user_list
from server.utils import get_user
from server.utils import save_measurement


@app.route('/rs/data/post/<device_id>/<data_string>', methods=['GET'])
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
    ip_addr = request.headers.get('X-Real-IP')
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


@app.route('/api/user/measurement', methods=['GET'])
def get_measurements_from_user_devices():
    """
    Gives dict of measurements for all user devices.
    :return:
    """
    if current_user.is_authenticated:
        devices = [device['uuid'] for device in get_devices_per_user(current_user.id)]
    else:
        devices = [device['uuid'] for device in get_all_devices()]

    response_data = get_measurements_by_count_for_devices(devices, TOTAL_COUNT)

    response = Response(response=json.dumps(response_data),
                        status=200,
                        mimetype="application/json")

    return response


@app.route('/api/measurement/<device_uuid>/', methods=['GET'])
@app.route('/api/measurement/<device_uuid>/<timestamp>', methods=['GET'])
def get_measurements_timestamp(device_uuid, timestamp=0):
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
    measurements = get_measurements_by_timestamp(device_id=device_uuid,
                                                 since=timestamp)

    response = Response(response=json.dumps(measurements),
                        status=200,
                        mimetype="application/json")

    return response


@app.route('/api/measurement/<device_uuid>/count/<count>', methods=['GET'])
def get_measurements_count(device_uuid, count=TOTAL_COUNT):
    """
    Get specified quantity of measurements from device,
    :param device_uuid
    :param count of measurements
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
    count = int(count)
    measurements = get_measurements_by_count(device_id=device_uuid,
                                             count=count)
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
    try:
        devices = get_devices_per_user(user_id)
    except Exception:
        return Response(status=404,
                        response="User not found")

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
    user = get_user(user_id=user_id)

    return Response(response=json.dumps(user),
                    status=200,
                    mimetype='application/json')
