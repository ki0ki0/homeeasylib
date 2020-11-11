import asyncio
from asyncio import Future
from typing import Any, Dict

import paho.mqtt.client as mqtt
from structlog import get_logger

from DeviceState import DeviceState
from EncryptedMqtt import EncryptedMqtt


logger = get_logger()


class HomeEasyLib:
    statuses: Dict[str, DeviceState] = dict()
    commands: Dict[str, DeviceState] = dict()
    futs: Dict[str, Future] = dict()
    dump: bool = False
    mqtt_client: EncryptedMqtt()

    def connect(self, host: str = "91.196.132.126", port: int = 1883):
        self.mqtt_client = EncryptedMqtt()
        self.mqtt_client.on_message_decrypted = self.on_message
        self.mqtt_client.connect(host, port)
        #  self.mqtt_client.loop_start()

    def on_message(self, _client: mqtt.Client, _userdata: Any, mac: str, decrypted: bytes, message: mqtt.MQTTMessage):
        logger.debug("message received", topic=message.topic, payload=message.payload.hex(), decrypted=decrypted.hex())
        if len(decrypted) == 0:
            return
        state = DeviceState(decrypted)
        if 'dev/status/' in message.topic:
            self.statuses[mac] = state
            if self.dump:
                logger.info("state received", topic=message.topic, state=state)

            if mac in self.futs:
                fut = self.futs[mac]
                fut.set_result(state)

        if 'dev/cmd/' in message.topic:
            self.commands[mac] = state
            logger.info("cmd received", topic=message.topic, state=state)

    def dump_status(self, mac: str, topic_prefix: str = 'dev/status/010202/'):
        self.dump = True
        topic = topic_prefix + mac
        self.mqtt_client.subscribe(topic)

    def dump_cmd(self, mac: str, topic_prefix: str = 'dev/cmd/010202/'):
        topic = topic_prefix + mac
        self.mqtt_client.subscribe(topic)

    def disconnect(self):
        self.mqtt_client.disconnect()

    def request_status(self, mac: str,
                       cmd_topic_prefix: str = 'dev/cmd/010202/',
                       status_topic_prefix: str = 'dev/status/010202/'):
        data = bytes([170, 170, 18, 160, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26])
        self.mqtt_client.subscribe(status_topic_prefix + mac)

        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        self.futs[mac] = fut

        self.mqtt_client.publish(cmd_topic_prefix + mac, data)
        return fut

    def send(self, mac: str, topic_prefix: str = 'dev/cmd/010202/'):
        if mac not in self.statuses:
            return None
        status = self.statuses[mac]
        self.mqtt_client.publish(topic_prefix + mac, status.cmd)

    def get(self, mac: str, key: str) -> Any:
        if mac not in self.statuses:
            return None
        status = self.statuses[mac]
        attr = getattr(status, key)
        return attr

    def set(self, mac: str, key: str, value: Any) -> Any:
        if mac not in self.statuses:
            return None
        status = self.statuses[mac]
        old = getattr(status, key)

        setattr(status, key, value)
        return old
