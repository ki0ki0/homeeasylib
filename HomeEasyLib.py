import logging
import sys
import time
from typing import Any

import paho.mqtt.client as mqtt
import structlog
from structlog import get_logger

from DeviceState import DeviceState
from EncryptedMqtt import EncryptedMqtt


logger = get_logger()


# noinspection PyUnusedLocal
def on_message(client: mqtt.Client, userdata: Any, mac: str, decrypted: bytes, message: mqtt.MQTTMessage):
    logger.info("message received", mac=mac, payload=message.payload.hex(), decrypted=decrypted.hex())
    state = DeviceState()
    if len(decrypted) == 0:
        return
    st = state.parse(decrypted)
    logger.info("State received", mac=mac, state=st)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO
    )
    structlog.configure(
         logger_factory=structlog.stdlib.LoggerFactory(),
    )

    mqtt = EncryptedMqtt()
    mqtt.on_message_decrypted = on_message
    mqtt.connect()
    mqtt.subscribe('#', 'dev/')
    mqtt.loop_start()
    time.sleep(30)
    mqtt.loop_stop()
    mqtt.disconnect()
