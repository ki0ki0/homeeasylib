import asyncio
from unittest import TestCase

import paho.mqtt.client as mqtt

from homeeasy.HomeEasyLib import HomeEasyLib


class TestHomeEasyLib(TestCase):
    def test_request_status_async(self):
        lib = HomeEasyLib()
        mac = "mac"
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.request_status_async_send_status_twice(lib, mac))
        loop.close()

    def request_status_async_send_status_twice(self, lib, mac):
        fut = lib.request_status_async(mac)
        message = mqtt.MQTTMessage(0, 'dev/status/'.encode('utf-8'))
        data = bytes([170, 170, 18, 0, 10, 10, 0, 12, 7, 0, 196, 0, 0, 0, 0, 22, 5, 0, 0, 0, 108])
        lib.on_message(None, None, mac, data, message)
        lib.on_message(None, None, mac, data, message)
        return fut
