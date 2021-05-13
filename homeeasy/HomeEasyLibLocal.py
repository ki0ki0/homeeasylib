import asyncio
import logging
from asyncio import StreamWriter, StreamReader
from typing import Any

from homeeasy.CustomLogger import CustomLogger
from homeeasy.DeviceState import DeviceState

logger = CustomLogger(logging.getLogger(__name__))


class HomeEasyLibLocal:
    _reader: StreamReader
    _writer: StreamWriter
    _state: DeviceState

    async def connect(self, host: str, port: int = 12416):
        self._reader, self._writer = await asyncio.open_connection(host, port)

    async def disconnect(self):
        self._writer.close()
        await self._writer.wait_closed()

    async def request_status_async(self):
        data = bytes([170, 170, 18, 160, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26])
        return await self._send(data)

    async def _send(self, data):
        self._writer.write(data)
        await self._writer.drain()
        data = await self._reader.read(4096)
        self._state = DeviceState(data)
        return self._state

    async def send(self, status: DeviceState = None):
        if status is None:
            status = self._state
        return await self._send(status.cmd)

    def get(self, key: str) -> Any:
        attr = getattr(self._state, key)
        return attr

    def set(self, key: str, value: Any) -> Any:
        old = getattr(self._state, key)

        setattr(self._state, key, value)
        return old
