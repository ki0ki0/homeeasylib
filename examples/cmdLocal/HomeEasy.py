import logging
from typing import List

from homeeasy import valueHelper
from homeeasy.HomeEasyLib import HomeEasyLib, DeviceState
from homeeasy.CustomLogger import CustomLogger
from homeeasy.HomeEasyLibLocal import HomeEasyLibLocal
from homeeasy.HomeEasyLibLocalDiscovery import HomeEasyLibLocalDiscovery

logger = CustomLogger(logging.getLogger(__name__))


class HomeEasy:
    _lib: HomeEasyLibLocal

    def __init__(self) -> None:
        self._lib = HomeEasyLibLocal()

    async def _status(self, ip: str) -> DeviceState:
        await self._lib.connect(ip)
        return await self._lib.request_status_async()

    async def _send(self) -> None:
        await self._lib.send()

    async def status(self, ip: str) -> None:
        status = await self._status(ip)
        print(f"{status}")

    async def get(self, ip: str, keys: List[str]) -> None:
        await self._status(ip)
        for key in keys:
            try:
                value = self._lib.get(key)
            except AttributeError:
                print(f"Invalid property {key}.")
                return
            print(f'{key} = {valueHelper.get_val(value)}')

    async def set(self, ip: str, pairs: List[List[str]]) -> None:
        await self._status(ip)
        for pair in pairs:
            key = pair[0]
            val = pair[1]

            try:
                old = self._lib.get(key)
            except AttributeError:
                print(f"Invalid property {key}.")
                return

            try:
                self._lib.set(key, val)
                new = self._lib.get(key)
            except ValueError:
                print(f"Invalid property value {val}.")
                return

            await self._send()

            print(f'{key} = {valueHelper.get_val(new)} (was {valueHelper.get_val(old)})')
