import random
import uuid

from config import DEVICE_COUNT
from config import SERVER_URL

from locust import Locust
from locust import TaskSet
from locust import task


devices = set()

for i in range(DEVICE_COUNT):
    device_uuid = uuid.uuid4()
    devices.add(device_uuid)


class MyTaskSet(TaskSet):
    @staticmethod
    def two_byte_hex(value):
        h = hex(value)

        return h[-4:]

    def get_random_data(self):
        gpio = random.randint(0, 10)
        power = random.randint(0, 10)
        voltage = random.randint(0, 20)
        temparature = random.randint(-10, 30)

        return self.two_byte_hex(gpio) + self.two_byte_hex(power) \
                                       + self.two_byte_hex(voltage) \
                                       + self.two_byte_hex(temparature)

    @task
    def send_measurement(self):
        url = "/rs/data/post/{device_id}/{data}"
        data = self.get_random_data()

        for device_id in devices:
            url = url.format(device_id=device_id,
                             data=data)
            
            r = self.client.get(url=url)
            print(r.content)


class MyLocust(Locust):
    task_set = MyTaskSet
    min_wait = 5000
    max_wait = 15000