import asyncio
import logging
from asyncio import Future
from typing import Any, Dict, Callable, Optional

import paho.mqtt.client as mqtt

from homeeasy.AsyncioHelper import AsyncioHelper
from homeeasy.CustomLogger import CustomLogger
from homeeasy.DeviceState import DeviceState
from homeeasy.EncryptedMqtt import EncryptedMqtt

logger = CustomLogger(logging.getLogger(__name__))


class HomeEasyLib:
    _cache: Dict[str, DeviceState] = dict()
    _statusCb: Dict[str, Callable[[str, DeviceState], None]] = dict()
    _statusFut: Dict[str, Future] = dict()
    _dump_status: Callable[[str, DeviceState], None] = None
    _dump_cmd: Callable[[str, DeviceState], None] = None
    _client: EncryptedMqtt
    _host: str
    _port: int

    def __init__(self) -> None:
        self._client = EncryptedMqtt()
        self._client.on_message = self.on_message
        self._client.on_disconnect = self.on_disconnect
        self._client.on_socket_close

        loop = None
        try:
            loop = asyncio.events.get_running_loop()
        except RuntimeError:
            pass

        if loop is not None:
            AsyncioHelper(self._client)

    def connect(self, host: str = "91.196.132.126", port: int = 1883):
        self._host = host
        self._port = port
        self._client.connect(host, port)

        loop = None
        try:
            loop = asyncio.events.get_running_loop()
        except RuntimeError:
            pass

        if loop is None:
            self._client.loop_start()

    def on_disconnect(self, client, userdata, reasonCode):
        logger.debug("disconnected", reasonCode=reasonCode)
        if reasonCode == mqtt.MQTT_ERR_SUCCESS:
            return
        self.connect(self._host, self._port)

    def on_message(self, _client: mqtt.Client, _userdata: Any, mac: str, decrypted: bytes, message: mqtt.MQTTMessage):
        logger.debug("message received", topic=message.topic, payload=message.payload.hex(), decrypted=decrypted.hex())
        if len(decrypted) == 0:
            return
        state = DeviceState(decrypted)
        if 'dev/status/' in message.topic:
            self._cache[mac] = state
            if self._dump_status is not None:
                self._dump_status(mac, state)

            if mac in self._statusCb:
                cb = self._statusCb[mac]
                cb(mac, state)

            if mac in self._statusFut:
                fut = self._statusFut.pop(mac)
                fut.set_result(state)

        if 'dev/cmd/' in message.topic:
            if self._dump_cmd is not None:
                self._dump_cmd(mac, state)

    def dump_status(self, mac: str, cb: Callable[[str, DeviceState], None], topic_prefix: str = 'dev/status/010202/'):
        self._dump_status = cb
        topic = topic_prefix + mac
        self._client.subscribe(topic)

    def dump_cmd(self, mac: str, cb: Callable[[str, DeviceState], None], topic_prefix: str = 'dev/cmd/010202/'):
        self._dump_cmd = cb
        topic = topic_prefix + mac
        self._client.subscribe(topic)

    def disconnect(self):
        self._client.disconnect()

    def request_status(self, mac: str, cb: Optional[Callable[[str, DeviceState], None]] = None,
                       cmd_topic_prefix: str = 'dev/cmd/010202/',
                       status_topic_prefix: str = 'dev/status/010202/'):

        if cb is not None:
            self._statusCb[mac] = cb

        if not self._client.is_connected():
            self.connect(self._host, self._port)

        self._client.subscribe(status_topic_prefix + mac)
        data = bytes([170, 170, 18, 160, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26])
        self._client.publish(cmd_topic_prefix + mac, data)

    def request_status_async(self, mac: str,
                             cmd_topic_prefix: str = 'dev/cmd/010202/',
                             status_topic_prefix: str = 'dev/status/010202/'):
        loop = asyncio.get_event_loop()
        fut = loop.create_future()

        self._statusFut[mac] = fut
        self.request_status(mac, None, cmd_topic_prefix, status_topic_prefix)
        return fut

    def send(self, mac: str, status: DeviceState = None, topic_prefix: str = 'dev/cmd/010202/'):
        if status is None:
            if mac not in self._cache:
                return None
            status = self._cache[mac]

        if not self._client.is_connected():
            self.connect(self._host, self._post)

        self._client.publish(topic_prefix + mac, status.cmd)

    def get(self, mac: str, key: str) -> Any:
        if mac not in self._cache:
            return None
        status = self._cache[mac]
        attr = getattr(status, key)
        return attr

    def set(self, mac: str, key: str, value: Any) -> Any:
        if mac not in self._cache:
            return None
        status = self._cache[mac]
        old = getattr(status, key)

        setattr(status, key, value)
        return old
