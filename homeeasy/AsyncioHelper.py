import asyncio
import logging

from paho.mqtt.client import Client, MQTT_ERR_SUCCESS

logger = logging.getLogger(__name__)


class AsyncioHelper:
    def __init__(self, client: Client):
        self.loop = asyncio.get_event_loop()
        self.client = client
        self.client.on_socket_open = self.on_socket_open
        self.client.on_socket_close = self.on_socket_close
        self.client.on_socket_register_write = self.on_socket_register_write
        self.client.on_socket_unregister_write = self.on_socket_unregister_write
        self.misc = None

    def on_socket_open(self, client, _userdata, sock):
        logger.debug("Socket opened")

        def cb():
            logger.debug("Socket is readable, calling loop_read")
            client.loop_read()

        self.loop.add_reader(sock, cb)
        self.misc = self.loop.create_task(self.misc_loop())

    def on_socket_close(self, _client, _userdata, sock):
        logger.debug("Socket closed")
        self.loop.remove_reader(sock)
        self.misc.cancel()

    def on_socket_register_write(self, client, _userdata, sock):
        logger.debug("Watching socket for writability.")

        def cb():
            logger.debug("Socket is writable, calling loop_write")
            client.loop_write()

        self.loop.add_writer(sock, cb)

    def on_socket_unregister_write(self, _client, _userdata, sock):
        logger.debug("Stop watching socket for writability.")
        self.loop.remove_writer(sock)

    async def misc_loop(self):
        logger.debug("misc_loop started")
        while self.client.loop_misc() == MQTT_ERR_SUCCESS:
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
        logger.debug("misc_loop finished")
