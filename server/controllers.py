from server import app


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


@app.route('/login', methods=['POST'])
def login():
    """
    Login user
    :return:
    """
    raise NotImplementedError()


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register new user in system.
    :return:
    """
    raise NotImplementedError()


@app.route('/', methods=['GET'])
def index():
    """
    Home page
    :return:
    """
    raise NotImplementedError()

