import random
import requests
import time


BASE_URL = "http://0.0.0.0:9000"
URL = "/rs/data/post/{0}/{1}"
DEVICE_ID = "abcd"


def main():
    base_Value = 50

    while True:
        gpio = "0000"
        voltage = "00" + hex(base_Value + random.randint(0, 60) - 30)[2:]
        power = "AAAA"
        temperature = "BBBB"
        data = gpio + voltage + power + temperature + "0000" * 4

        url = BASE_URL + URL.format(DEVICE_ID, data)
        response = requests.get(url)
        print("Status code: {0}".format(response.status_code))
        time.sleep(1)


if __name__ == "__main__":
    main()
