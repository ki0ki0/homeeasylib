from typing import Any

import paho.mqtt.client as mqtt
from structlog import get_logger

from DeviceStateParser import DeviceStateParser
from EncryptedMqtt import EncryptedMqtt


logger = get_logger()


class HomeEasyLib:

    def __init__(self):
        self.mqtt = EncryptedMqtt()

    def connect(self, host: str = "91.196.132.126", port: int = 1883):
        self.mqtt.on_message_decrypted = self.on_message
        self.mqtt.connect(host, port)
        self.mqtt.loop_start()

    # noinspection PyMethodMayBeStatic
    def on_message(self, client: mqtt.Client, userdata: Any, mac: str, decrypted: bytes, message: mqtt.MQTTMessage):
        logger.debug("message received", topic=message.topic, payload=message.payload.hex(), decrypted=decrypted.hex())
        if len(decrypted) == 0:
            return
        state = DeviceStateParser()
        st = state.parse(decrypted)
        logger.info("state received", topic=message.topic, state=st)

    def dump_status(self, mac: str, topic_prefix: str = 'dev/status/010202/'):
        topic = topic_prefix + mac
        self.mqtt.subscribe(topic)

    def dump_cmd(self, mac: str, topic_prefix: str = 'dev/cmd/010202/'):
        topic = topic_prefix + mac
        self.mqtt.subscribe(topic)

    def disconnect(self):
        self.mqtt.loop_stop()
        self.mqtt.disconnect()

    def request_status(self, mac:str, topic_prefix: str = 'dev/cmd/010202/'):
        data = bytes([170, 170, 18, 160, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26])
        self.mqtt.publish(topic_prefix + mac, data)
