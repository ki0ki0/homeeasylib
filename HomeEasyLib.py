import time
from typing import Any

import paho.mqtt.client as mqtt

from DeviceState import DeviceState
from EncryptedMqtt import EncryptedMqtt


# noinspection PyUnusedLocal
def on_message(client: mqtt.Client, userdata: Any, mac: str, decrypted: bytes, message: mqtt.MQTTMessage):
    print(f"{mac}({len(message.payload)}): {message.payload.hex()} {decrypted.hex()}")
    state = DeviceState()
    if len(decrypted) == 0:
        return
    st = state.parse(decrypted)
    print(st)


if __name__ == '__main__':
    mqtt = EncryptedMqtt()
    mqtt.on_message_decrypted = on_message
    mqtt.connect()
    mqtt.subscribe('#', 'dev/')
    mqtt.loop_start()
    time.sleep(30)
    mqtt.loop_stop()
    mqtt.disconnect()
