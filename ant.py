from openant.easy.node import Node
from openant.devices import ANTPLUS_NETWORK_KEY
from openant.devices.bike_speed_cadence import (
    BikeSpeed,
    BikeCadence,
    BikeSpeedCadence,
    BikeSpeedData,
    BikeCadenceData,
)

from openant.devices.power_meter import (
    PowerData,
    PowerMeter
)
from openant.devices.heart_rate import (
    HeartRate,
    HeartRateData
)

WHEEL_CIRCUMFERENCE_M = 2.3


def get_device_listener(device_id=0):
    node = Node()
    node.set_network_key(0x00, ANTPLUS_NETWORK_KEY)

    device = HeartRate(node, device_id=device_id)

    def on_found():
        print(f"Device {device} found and receiving")

    def on_device_data(page: int, page_name: str, data):
        if isinstance(data, HeartRateData):
            print(f"HR: {data.heart_rate}", flush=True)
            

    device.on_found = on_found
    device.on_device_data = on_device_data
    return node

def main(device_id=0):
    # import logging
    # logging.basicConfig(level=logging.DEBUG)

    node = Node()
    node.set_network_key(0x00, ANTPLUS_NETWORK_KEY)

    device = HeartRate(node, device_id=device_id)

    def on_found():
        print(f"Device {device} found and receiving")

    def on_device_data(page: int, page_name: str, data):
        if isinstance(data, HeartRateData):
            print(f"HR: {data.heart_rate}", flush=True)
            

    device.on_found = on_found
    device.on_device_data = on_device_data

    try:
        print(f"Starting {device}, press Ctrl-C to finish")
        node.start()
    except KeyboardInterrupt:
        print("Closing ANT+ device...")
    finally:
        device.close_channel()
        node.stop()


if __name__ == "__main__":
    main()