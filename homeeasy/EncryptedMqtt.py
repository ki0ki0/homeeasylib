import logging
from typing import Any, Callable, Dict
import paho.mqtt.client as mqtt
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import pad

from homeeasy.CustomLogger import CustomLogger

logger = CustomLogger(logging.getLogger(__name__))


class EncryptedMqtt(mqtt.Client):
    _keys: Dict[str, bytes]

    def __init__(self, client_id="", clean_session=None, userdata=None,
                 protocol=mqtt.MQTTv311, transport="tcp"):
        super().__init__(client_id, clean_session, userdata, protocol, transport)
        self._keys = dict()

    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        mac: str = self._mac_from_topic(topic)
        key = self._key_for_mac(mac)
        encrypted = self._encrypt(payload, key)
        return super().publish(topic, encrypted, qos, retain, properties)

    @property
    def on_message(self):
        return self._on_message_internal

    @on_message.setter
    def on_message(self, func: Callable[[mqtt.Client, Any, str, bytes, mqtt.MQTTMessage], None]):
        mqtt.Client.on_message.fset(self, func)

    def _on_message_internal(self, client, userdata, message):
        logger.debug("message received", topic=message.topic, payload=message.payload.hex())
        mac: str = self._mac_from_topic(message.topic)
        key = self._key_for_mac(mac)

        decrypted = self._decrypt(message.payload, key) if len(message.payload) > 0 else message.payload
        logger.debug("message decrypted", topic=message.topic, decrypted=decrypted.hex())
        super().on_message(client, userdata, mac, decrypted, message)

    def _key_for_mac(self, mac):
        if mac not in self._keys:
            key = self._get_key(mac)
            logger.debug("key generated", mac=mac, key=key.decode("utf-8"))
            self._keys[mac] = key
        else:
            key = self._keys[mac]
            logger.debug("key exists", mac=mac, key=key.decode("utf-8"))
        return key

    # noinspection PyMethodMayBeStatic
    def _mac_from_topic(self, topic):
        return topic.split('/')[-1]

    # noinspection PyMethodMayBeStatic
    def _decrypt(self, enc: bytes, key: bytes) -> bytes:
        iv = key[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        dec = cipher.decrypt(enc)
        return dec  # unpad(dec, AES.block_size)

    @staticmethod
    def _encrypt(data: bytes, key: bytes) -> bytes:
        iv = key[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(data, AES.block_size))

    @staticmethod
    def _get_key(mac: str) -> bytes:
        magic_odd = '2Y10-6012-Y4'
        result = mac[::2]
        result += magic_odd

        h: MD5 = MD5.new()
        h.update(result.encode('utf-8'))
        result = h.hexdigest()[8: 24]

        return result.encode('utf-8')
