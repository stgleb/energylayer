import json

from flask import Response
from flask import request

from server import app
from server import get_or_create_device
from server import get_measurements_from_device
from server import get_devices_per_user
from server import get_user_list
from server import get_user
from server import save_measurement


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
