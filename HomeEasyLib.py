import logging
import sys
import time
from typing import Any

import paho.mqtt.client as mqtt
from structlog import get_logger

from DeviceStateParser import DeviceStateParser
from EncryptedMqtt import EncryptedMqtt


logger = get_logger()


class HomeEasyLib():

    # noinspection PyUnusedLocal
    def __init__(self):
        self.mqtt = EncryptedMqtt()

    def on_message(self, client: mqtt.Client, userdata: Any, mac: str, decrypted: bytes, message: mqtt.MQTTMessage):
        # logger.info("message received", mac=mac, payload=message.payload.hex(), decrypted=decrypted.hex())
        state = DeviceStateParser()
        if len(decrypted) == 0:
            return
        # st = state.parse2dict(decrypted)
        # logger.info("State received", state=st)
        st = state.parse(decrypted)
        logger.info("State received", mac=mac, state=st)

    def receive(self, mac, topic_prefix='dev/status/010202/'):
        self.mqtt.on_message_decrypted = self.on_message
        self.mqtt.connect()
        self.mqtt.subscribe(mac, topic_prefix)
        self.mqtt.loop_start()

    def stop(self):
        self.mqtt.loop_stop()
        self.mqtt.disconnect()

    def request_status(self, mac, topic_prefix='dev/cmd/010202/'):
        b = bytes([170, 170, 18, 160, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26])
        key = EncryptedMqtt.get_key(mac)
        encrypted = self.mqtt.encrypt(b, key)
        self.mqtt.publish(topic_prefix + mac, encrypted)