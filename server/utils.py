import hashlib

from datetime import datetime
from flask import request, url_for
from server.persistence.models import db, User, Device, Measurement


def hash_password(password):
    encoded = password.encode('utf-8')
    return hashlib.md5(encoded).hexdigest()


def register_user(form):
    user = None

    try:
        password_hash = hash_password(form.password.data)

        user = User(email=form.email.data,
                    password=password_hash,
                    username=form.username.data,
                    first_name=form.firstname.data,
                    last_name=form.lastname.data)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return user


def compare_password(user, password):
    return user.password == hash_password(password)


def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()

    return user


def update_user_profile(form, user_id, image_data=None):
    try:
        user = User.query.filter_by(id=user_id).first()

        if form.email.data:
            user.email = form.email.data

        if form.firstname.data:
            user.first_name = form.firstname.data

        if form.lastname.data:
            user.last_name = form.lastname.data

        if form.username.data:
            user.username = form.username.data

        if form.email.data:
            user.email = form.email.data

        if image_data:
            user.avatar_image = image_data.stream.read()

        db.session.commit()
    except Exception as e:
        db.session.rollback()


def get_or_create_device(device_id, device_ip=None):
    device = Device.query.filter_by(uuid=device_id).first()

    if device:
        if not device.ip_addr or device.ip_addr != device_ip:
            device.ip_addr = device_ip
            db.session.commit()

        return device

    try:
        device = Device(uuid=device_id, ip_addr=device_ip)
        db.session.add(device)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return device


def save_measurement(device, gpio, voltage, power, temperature):
    measurement = Measurement(device_id=device.id,
                              gpio=gpio,
                              voltage=voltage,
                              power=power,
                              temperature=temperature)

    try:
        db.session.add(measurement)
        device.measurements.append(measurement)
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def measurements_to_dto(measurements, count=20, offset=1):
    def measurement_to_dto(m):
        date = str(datetime.fromtimestamp(m.timestamp))

        return {
            "voltage": m.voltage,
            "power": m.power,
            "temperature": m.temperature,
            "gpio": m.gpio,
            "timestamp": m.timestamp,
            "date": date
        }

    measurements_dto = []

    for i in range(len(measurements)):
        measurements_dto.append(measurement_to_dto(measurements[i]))
        measurements_dto[i]['position'] = (offset - 1) * count + i + 1

    return measurements_dto


def get_measurements_by_timestamp(device_id, since=0):
    device = Device.query.filter_by(uuid=device_id).first()
    measurements = Measurement.query.filter_by(device_id=device.id).all()
    measurements = [m for m in measurements if m.timestamp > int(since)]

    return measurements_to_dto(measurements)


def get_measurements_by_count(device_id, count, offset=0):
    """
    Get specific count of measurements

    :param device_id: uuid of device
    :param count: count of measurements
    :param offset: offset in page.
    :return: list of measurements dto
    """
    device = Device.query.filter_by(uuid=device_id).first()

    measurements = Measurement.query.filter_by(device_id=device.id).all()
    measurements = measurements[-count:]

    return measurements_to_dto(measurements, count=count, offset=offset)


def get_all_measurements_count(device_id):
    """
    Get specific count of measurements

    :param device_id: uuid of device
    :return: count of measurements
    """
    device = Device.query.filter_by(uuid=device_id).first()

    return Measurement.query.filter_by(device_id=device.id).count()


def get_devices_per_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return Exception('User not found')

    def device_to_dto(device):
        return {
            "uuid": device.uuid,
            "ip_addr": device.ip_addr
        }

    return [device_to_dto(d) for d in user.devices]


def get_all_devices():
    devices = Device.query.all()

    def device_to_dto(device):
        return {
            "uuid": device.uuid,
            "ip_addr": device.ip_addr
        }

    devices = [device_to_dto(d) for d in devices]

    return devices


def get_user_list():
    users = User.query.all()

    def user_to_dto(user):
        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }

    return [user_to_dto(u) for u in users]


def attach_device_to_user(user_id, device_id):
    device = get_or_create_device(device_id=device_id)
    if device.user_id is not None:
        raise Exception("Device is already in use")

    user = User.query.filter_by(id=user_id).first()

    try:
        user.devices.append(device)
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def dettach_device_from_user(user_id, device_id):
    device = get_or_create_device(device_id=device_id)

    if device.user_id is None \
            or device.user_id != user_id:
        raise Exception("Device doesnt belong to user")

    user = User.query.filter_by(id=user_id).first()

    try:
        user.devices.remove(device)
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    user_dto = dict()
    user_dto['username'] = user.username
    user_dto['first_name'] = user.first_name
    user_dto['last_name'] = user.last_name
    user_dto['email'] = user.email
    user_dto['devices'] = get_devices_per_user(user_id=user_id)

    return user_dto


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

