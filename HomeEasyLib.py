from typing import Any, Dict

import paho.mqtt.client as mqtt
from structlog import get_logger

from DeviceState import DeviceState
from DeviceStateParser import DeviceStateParser
from EncryptedMqtt import EncryptedMqtt


logger = get_logger()


class HomeEasyLib:
    statuses: Dict[str, DeviceState]
    commands: Dict[str, DeviceState]

    def __init__(self):
        self.mqtt = EncryptedMqtt()
        self.commands = dict()
        self.statuses = dict()

    def connect(self, host: str = "91.196.132.126", port: int = 1883):
        self.mqtt.on_message_decrypted = self.on_message
        self.mqtt.connect(host, port)
        self.mqtt.loop_start()

    # noinspection PyMethodMayBeStatic
    def on_message(self, client: mqtt.Client, userdata: Any, mac: str, decrypted: bytes, message: mqtt.MQTTMessage):
        logger.debug("message received", topic=message.topic, payload=message.payload.hex(), decrypted=decrypted.hex())
        if len(decrypted) == 0:
            return
        parser = DeviceStateParser()
        state = parser.parse(decrypted)
        logger.info("state received", topic=message.topic, state=state)
        if 'dev/status/' in message.topic:
            self.statuses[mac] = state

        if 'dev/cmd/' in message.topic:
            self.commands[mac] = state

    def dump_status(self, mac: str, topic_prefix: str = 'dev/status/010202/'):
        topic = topic_prefix + mac
        self.mqtt.subscribe(topic)

    def dump_cmd(self, mac: str, topic_prefix: str = 'dev/cmd/010202/'):
        topic = topic_prefix + mac
        self.mqtt.subscribe(topic)

    def disconnect(self):
        self.mqtt.loop_stop()
        self.mqtt.disconnect()

    def request_status(self, mac: str,
                       cmd_topic_prefix: str = 'dev/cmd/010202/',
                       status_topic_prefix: str = 'dev/status/010202/'):
        data = bytes([170, 170, 18, 160, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26])
        self.mqtt.subscribe(status_topic_prefix + mac)
        self.mqtt.publish(cmd_topic_prefix + mac, data)

    def get(self, mac: str, key: str):
        if mac in self.statuses:
            status = self.statuses[mac]
            return getattr(status, key)

        return None
