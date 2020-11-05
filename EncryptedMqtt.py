import threading
from collections.abc import Callable
from typing import Any

import paho.mqtt.client as mqtt
from Crypto.Cipher import AES
from Crypto.Hash import MD5

from structlog import get_logger


logger = get_logger()


# noinspection PyUnusedLocal
def _on_message_decrypted_stub(client: mqtt.Client, userdata: Any, mac: str, decrypted: bytes,
                               message: mqtt.MQTTMessage):
    pass


class EncryptedMqtt(mqtt.Client):

    _on_message_decrypted: Callable[[mqtt.Client, Any, str, bytes, mqtt.MQTTMessage], None]
    _callback_mutex_decrypted: threading.RLock
    _keys: dict[str, bytes]

    def __init__(self, client_id="", clean_session=None, userdata=None,
                 protocol=mqtt.MQTTv311, transport="tcp"):
        super().__init__(client_id, clean_session, userdata, protocol, transport)
        self._keys = dict()
        self._callback_mutex_decrypted = threading.RLock()
        self._on_message_decrypted = _on_message_decrypted_stub

    def connect(self, host="91.196.132.126", port=1883, keepalive=60, bind_address="", bind_port=0,
                clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY, properties=None):
        logger.debug("connect", host=host, port=port)
        return super().connect(host, port, keepalive, bind_address, bind_port, clean_start, properties)

    def subscribe(self, mac, topic_prefix='dev/cmd/010202/', qos=0, options=None, properties=None):
        topic = topic_prefix + mac
        logger.debug("subscribe", topic=topic)
        super().subscribe(topic)
        self.on_message = self.on_message_internal

    @property
    def on_message_decrypted(self):
        return self._on_message_decrypted

    @on_message_decrypted.setter
    def on_message_decrypted(self, func: Callable[[mqtt.Client, Any, str, bytes, mqtt.MQTTMessage], None]):
        with self._callback_mutex_decrypted:
            self._on_message_decrypted = func

    def on_message_internal(self, client, userdata, message):
        mac: str = message.topic.split('/')[-1]
        logger.debug("message received", topic=message.topic, payload=message.payload.hex())
        if mac not in self._keys:
            key = self.get_key(mac)
            logger.debug("key generated", mac=mac, key=key.decode("utf-8"))
            self._keys[mac] = key
        else:
            key = self._keys[mac]
            logger.debug("key exists", mac=mac, key=key.decode("utf-8"))

        decrypted = self.decrypt(message.payload, key) if len(message.payload) > 0 else message.payload
        logger.debug("message decrypted", topic=message.topic, decrypted=decrypted.hex())
        self.on_message_decrypted(client, userdata, mac, decrypted, message)

    def decrypt(self, enc: bytes, key: bytes) -> bytes:
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        dec = cipher.decrypt(enc)
        return self._unpad(dec)

    @staticmethod
    def get_key(mac: str) -> bytes:
        magic_odd = '2Y10-6012-Y4'
        result = mac[::2]
        result += magic_odd

        h: MD5 = MD5.new()
        h.update(result.encode('utf-8'))
        result = h.hexdigest()[8: 24]

        return result.encode('utf-8')

    @staticmethod
    def _unpad(s: bytes) -> bytes:
        return s[:-ord(s[len(s) - 1:])]
