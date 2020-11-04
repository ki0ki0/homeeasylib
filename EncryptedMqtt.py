import threading
import paho.mqtt.client as mqtt
from Crypto.Cipher import AES
from Crypto.Hash import MD5


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]


class EncryptedMqtt(mqtt.Client):

    def __init__(self, client_id="", clean_session=None, userdata=None,
                 protocol=mqtt.MQTTv311, transport="tcp"):
        super().__init__(client_id, clean_session, userdata, protocol, transport)
        self._keys = dict()
        self._callback_mutex_decrypted = threading.RLock()
        self._on_message_decrypted = None

    def connect(self, host="91.196.132.126", port=1883, keepalive=60, bind_address="", bind_port=0,
                clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY, properties=None):
        return super().connect(host, port, keepalive, bind_address, bind_port, clean_start, properties)

    def subscribe(self, mac, topic='dev/cmd/010202/', qos=0, options=None, properties=None):
        super().subscribe(topic + mac)
        self.on_message = self.on_message_internal

    @property
    def on_message_decrypted(self):
        return self._on_message_decrypted

    @on_message_decrypted.setter
    def on_message_decrypted(self, func):
        with self._callback_mutex_decrypted:
            self._on_message_decrypted = func

    def on_message_internal(self, client, userdata, message):
        mac = message.topic.split('/')[-1]
        if mac not in self._keys:
            self._keys[mac] = self.get_key(mac)

        key = self._keys[mac]
        decrypted = self.decrypt(message.payload, key) if len(message.payload) > 0 else message.payload
        self.on_message_decrypted(client, userdata, mac, decrypted, message)

    @staticmethod
    def decrypt(enc, key):
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        dec = cipher.decrypt(enc)
        return _unpad(dec)

    @staticmethod
    def get_key(mac):
        magic_odd = '2Y10-6012-Y4'
        result = mac[::2]
        result += magic_odd

        h = MD5.new()
        h.update(result.encode('utf-8'))
        result = h.hexdigest()[8: 24]

        return result.encode('utf-8')
