import random
import requests
import time


BASE_URL = "http://0.0.0.0:9000"
URL = "/rs/data/post/{0}/{1}"
devices = ["abcd", "efgh", "ijkl"]


def main():
    base_Value = 50
    deviation = 30

    while True:
        for device in devices:
            gpio = "0000"
            voltage = "00" + hex(base_Value +
                                 random.randint(0, deviation) -
                                 deviation / 2)[2:]
            power = "00" + hex(base_Value +
                               random.randint(0, deviation) -
                               deviation / 2)[2:]
            temperature = "00" + hex(base_Value +
                                     random.randint(0, deviation) -
                                     deviation / 2)[2:]
            data = gpio + voltage + power + temperature + "0000" * 4

            url = BASE_URL + URL.format(device, data)
            response = requests.get(url)
            print("Status code: {0}".format(response.status_code))
            time.sleep(1)


if __name__ == "__main__":
    main()
