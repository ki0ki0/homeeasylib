import asyncio
from asyncio import Future
from typing import Any, Dict, Callable

import paho.mqtt.client as mqtt
from structlog import get_logger

from HomeEasyLib.AsyncioHelper import AsyncioHelper
from HomeEasyLib.DeviceState import DeviceState
from HomeEasyLib.EncryptedMqtt import EncryptedMqtt

logger = get_logger()


class HomeEasyLib:
    cache: Dict[str, DeviceState] = dict()
    status: Dict[str, Callable[[str, DeviceState], None]] = dict()
    _dump_status: Callable[[str, DeviceState], None] = None
    _dump_cmd: Callable[[str, DeviceState], None] = None
    mqtt_client: EncryptedMqtt

    def __init__(self) -> None:
        self.mqtt_client = EncryptedMqtt()
        self.mqtt_client.on_message_decrypted = self.on_message

        loop = None
        try:
            loop = asyncio.events.get_running_loop()
        except RuntimeError:
            pass

        if loop is not None:
            AsyncioHelper(self.mqtt_client)

    def connect(self, host: str = "91.196.132.126", port: int = 1883):
        self.mqtt_client.connect(host, port)

        loop = None
        try:
            loop = asyncio.events.get_running_loop()
        except RuntimeError:
            pass

        if loop is None:
            self.mqtt_client.loop_start()

    def on_message(self, _client: mqtt.Client, _userdata: Any, mac: str, decrypted: bytes, message: mqtt.MQTTMessage):
        logger.debug("message received", topic=message.topic, payload=message.payload.hex(), decrypted=decrypted.hex())
        if len(decrypted) == 0:
            return
        state = DeviceState(decrypted)
        if 'dev/status/' in message.topic:
            self.cache[mac] = state
            if self._dump_status is not None:
                self._dump_status(mac, state)

            if mac in self.status:
                cb = self.status[mac]
                cb(mac, state)

        if 'dev/cmd/' in message.topic:
            if self._dump_cmd is not None:
                self._dump_cmd(mac, state)

    def dump_status(self, mac: str, cb: Callable[[str, DeviceState], None], topic_prefix: str = 'dev/status/010202/'):
        self._dump_status = cb
        topic = topic_prefix + mac
        self.mqtt_client.subscribe(topic)

    def dump_cmd(self, mac: str, cb: Callable[[str, DeviceState], None], topic_prefix: str = 'dev/cmd/010202/'):
        self._dump_cmd = cb
        topic = topic_prefix + mac
        self.mqtt_client.subscribe(topic)

    def disconnect(self):
        self.mqtt_client.disconnect()

    def request_status(self, mac: str, cb: Callable[[str, DeviceState], None],
                       cmd_topic_prefix: str = 'dev/cmd/010202/',
                       status_topic_prefix: str = 'dev/status/010202/'):
        self.status[mac] = cb

        data = bytes([170, 170, 18, 160, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26])
        self.mqtt_client.subscribe(status_topic_prefix + mac)
        self.mqtt_client.publish(cmd_topic_prefix + mac, data)

    def request_status_async(self, mac: str,
                             cmd_topic_prefix: str = 'dev/cmd/010202/',
                             status_topic_prefix: str = 'dev/status/010202/'):
        loop = asyncio.get_running_loop()
        fut = loop.create_future()

        self.request_status(mac, lambda _, state: fut.set_result(state), cmd_topic_prefix, status_topic_prefix)
        return fut

    def send(self, mac: str, topic_prefix: str = 'dev/cmd/010202/'):
        if mac not in self.cache:
            return None
        status = self.cache[mac]
        self.mqtt_client.publish(topic_prefix + mac, status.cmd)

    def get(self, mac: str, key: str) -> Any:
        if mac not in self.cache:
            return None
        status = self.cache[mac]
        attr = getattr(status, key)
        return attr

    def set(self, mac: str, key: str, value: Any) -> Any:
        if mac not in self.cache:
            return None
        status = self.cache[mac]
        old = getattr(status, key)

        setattr(status, key, value)
        return old
