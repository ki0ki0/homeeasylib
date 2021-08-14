import asyncio
import logging
from asyncio import StreamWriter, StreamReader, Task
from typing import Any

from homeeasy.CustomLogger import CustomLogger
from homeeasy.DeviceState import DeviceState

logger = CustomLogger(logging.getLogger(__name__))


class HomeEasyLibLocal:
    _reader: StreamReader = None
    _writer: StreamWriter = None
    _readTask: Task = None
    _state: DeviceState = None
    _host: str = ""
    _port: int = 0

    def __init__(self, loop, callback) -> None:
        self._loop = loop
        self._callback = callback

    async def connect(self, host: str, port: int = 12416):
        self._host = host
        self._port = port
        await self._reconnect()

    async def _read_async(self):
        while True:
            resp = await self._reader.read(21)
            if not resp:
                await self._reconnect()
                return

            if not len(resp) == 21:
                continue
            self._state = DeviceState(resp)
            await self._callback(self._state)

    async def _reconnect(self):
        await self.disconnect()
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port)
        self._readTask = self._loop.create_task(self._read_async())

    async def disconnect(self):
        if self._writer is not None:
            try:
                self._readTask.cancel()
            except:
                pass

            try:
                self._writer.close()
                await self._writer.wait_closed()
            except:
                pass
            self._writer = None

    async def request_status_async(self):
        data = bytes([170, 170, 18, 160, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26])
        return await self._send(data)

    async def _send(self, data):
        retry = 0
        while retry < 3:
            retry = retry + 1
            try:
                self._writer.write(data)
                await self._writer.drain()
                break
            except:
                if retry < 3:
                    await self._reconnect()
                else:
                    raise

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
