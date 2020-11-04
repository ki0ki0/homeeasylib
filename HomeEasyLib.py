import time

from DeviceState import DeviceState
from EncryptedMqtt import EncryptedMqtt


def on_message(client, userdata, mac, decrypted, message):
    print(f"{mac}({len(message.payload)}): {decrypted.hex()}")
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
