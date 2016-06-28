import time
import logging
from sqlalchemy import desc
from sqlalchemy import and_

from server import db
from server import Measurement
from server.config import DEVICE_INTERVAL
from server.persistence.models import Hour
from server.persistence.models import Device
from server.persistence.models import Day
from server.persistence.models import Week
from tasks.celery_app import app
from tasks.config import HOUR_INTERVAL
from tasks.config import DAYS_INTERVAL
from tasks.config import WEEK_INTERVAL

logger = logging.getLogger(__name__)


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
    channel_len = int(interval / DEVICE_INTERVAL)
    # count of channels
    channel_count = int(len(measurements) / channel_len)

    for i in range(channel_count):
        tmp = measurements[i * channel_len: (i + 1) * channel_len]
        dto = avg(tmp)
        result.append(dto)

    return result


@app.task(queue="hour")
def hourly():
    """
    Run command: celery -A tasks worker -B -l info -Q hour -n worker1
    :return:
    """
    devices = Device.query.all()

    for device in devices:
        try:
            lastest_aggregate = Hour.query.filter(Hour.device_id == device.id). \
                order_by(desc(Hour.timestamp)).first()

            if lastest_aggregate:
                latest_timestamp = lastest_aggregate.timestamp
            else:
                first_measurement = Measurement.query.filter(Measurement.device_id == device.id).\
                    order_by(Measurement.timestamp).first()
                try:
                    latest_timestamp = first_measurement.timestampp
                except Exception:
                    latest_timestamp = 0

            measurements = Measurement.query. \
                filter(and_(Measurement.timestamp > latest_timestamp,
                            Measurement.device_id == device.id)). \
                order_by(desc(Measurement.timestamp)).all()
            aggregated = aggregate(measurements, HOUR_INTERVAL)

            for a in aggregated:
                h = Hour(device_id=device.id,
                         voltage=a["voltage"],
                         power=a["power"],
                         temperature=a["temperature"],
                         timestamp=latest_timestamp)
                latest_timestamp += HOUR_INTERVAL
                db.session.add(h)
            # Save aggregated data for device
            db.session.commit()
        except Exception:
            logger.exception("Exception has been occured ")


@app.task(queue="day")
def daily():
    """
    Run command: celery -A tasks worker -B -l info -Q day -n worker2
    :return:
    """
    devices = Device.query.all()

    for device in devices:
        try:
            lastest_aggregate = Day.query.filter(Day.device_id == device.id). \
                order_by(desc(Day.timestamp)).first()

            if lastest_aggregate:
                latest_timestamp = lastest_aggregate.timestamp
            else:
                first_measurement = Measurement.query.filter(Measurement.device_id == device.id).\
                    order_by(Measurement.timestamp).first()
                try:
                    latest_timestamp = first_measurement.timestampp
                except Exception:
                    latest_timestamp = 0

            measurements = Measurement.query. \
                filter(and_(Measurement.timestamp > latest_timestamp,
                            Measurement.device_id == device.id)). \
                order_by(desc(Measurement.timestamp)).all()
            aggregated = aggregate(measurements, DAYS_INTERVAL)

            for a in aggregated:
                d = Day(device_id=device.id,
                        voltage=a["voltage"],
                        power=a["power"],
                        temperature=a["temperature"],
                        timestamp=latest_timestamp)
                latest_timestamp += DAYS_INTERVAL
                db.session.add(d)
            # Save aggregated data for device
            db.session.commit()
        except Exception:
            logger.exception("Exception has been occured")


@app.task(queue="week")
def weekly():
    """
    Run command: celery -A tasks worker -B -l info -Q week -n worker3
    :return:
    """
    devices = Device.query.all()

    for device in devices:
        try:
            lastest_aggregate = Week.query.filter(Week.device_id == device.id). \
                order_by(desc(Week.timestamp)).first()

            if lastest_aggregate:
                latest_timestamp = lastest_aggregate.timestamp
            else:
                first_measurement = Measurement.query.filter(Measurement.device_id == device.id).\
                    order_by(Measurement.timestamp).first()
                try:
                    latest_timestamp = first_measurement.timestampp
                except Exception:
                    latest_timestamp = 0

            measurements = Measurement.query. \
                filter(and_(Measurement.timestamp > latest_timestamp,
                            Measurement.device_id == device.id)). \
                order_by(desc(Measurement.timestamp)).all()
            aggregated = aggregate(measurements, WEEK_INTERVAL)

            for a in aggregated:
                w = Week(device_id=device.id,
                         voltage=a["voltage"],
                         power=a["power"],
                         temperature=a["temperature"],
                         timestamp=latest_timestamp)
                latest_timestamp += WEEK_INTERVAL
                db.session.add(w)
            # Save aggregated data for device
            db.session.commit()
        except Exception:
            logger.exception("Exception has been occured ")


if __name__ == "__main__":
    hourly()
    daily()
    weekly()
