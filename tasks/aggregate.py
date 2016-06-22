import time
from sqlalchemy import desc


from server import db
from server import Measurement
from server.config import DEVICE_INTERVAL
from server.persistence.models import Hour
from server.persistence.models import Day
from server.persistence.models import Week
from tasks.celery_app import app
from tasks.config import HOUR_INTERVAL
from tasks.config import DAYS_INTERVAL
from tasks.config import WEEK_INTERVAL


def unix_time():
    return int(time.time())


def avg(measurements):
    dto = {
            "voltage": 0,
            "power": 0,
            "temperature": 0,
    }

    for m in measurements:
        dto["voltage"] += m.voltage
        dto["power"] += m.power
        dto["temperature"] = m.temperature

    dto["voltage"] /= len(measurements)
    dto["power"] /= len(measurements)
    dto["temperature"] /= len(measurements)

    return dto


def aggregate(measurements, interval):
    result = []
    # channel width
    cnt = interval / DEVICE_INTERVAL
    # count of channels
    channel_count = int(len(measurements) / cnt)

    for i in range(channel_count):
        tmp = measurements[i * cnt: (i + 1) * cnt]
        dto = avg(tmp)
        result.append(dto)

    return result


@app.task(queue="hour")
def hourly():
    """
    Run command: celery -A tasks worker -B -l info -Q hour -n worker1
    :return:
    """
    lastest_aggregate = Hour.query.\
        order_by(desc(Hour.timestamp)).first()
    latest_timestamp = 0

    if lastest_aggregate:
        latest_timestamp = lastest_aggregate.timestamp

    measurements = Measurement.query.\
        filter_by(Measurement.timestamp > latest_timestamp).\
        order_by(desc(Measurement.timestamp)).all()
    aggregated = aggregate(measurements, HOUR_INTERVAL)

    for a in aggregated:
        Hour()


@app.task(queue="day")
def daily():
    """
    Run command: celery -A tasks worker -B -l info -Q day -n worker2
    :return:
    """
    lastest_measurement = Measurement.query.\
        filter_by(desc(Measurement.timestamp)).first()
    print("Hello, i am second")


@app.task(queue="week")
def weekly():
    """
    Run command: celery -A tasks worker -B -l info -Q week -n worker2
    :return:
    """
    lastest_measurement = Measurement.query. \
        filter_by(desc(Measurement.timestamp)).first()

    print("Hello, i am third")


if __name__ == "__main__":
    hourly()
