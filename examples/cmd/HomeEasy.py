from typing import List

from structlog import get_logger

from homeeasy import valueHelper
from homeeasy.HomeEasyLib import HomeEasyLib, DeviceState

logger = get_logger()


class HomeEasy:
    _lib: HomeEasyLib

    def __init__(self) -> None:
        self._lib = HomeEasyLib()

    async def _status(self, mac: str) -> DeviceState:
        self._lib.connect()
        return await self._lib.request_status_async(mac)

    def _send(self, mac: str) -> None:
        self._lib.send(mac)

    async def status(self, mac: str) -> None:
        status = await self._status(mac)
        print(f"{status}")

    async def get(self, mac: str, keys: List[str]) -> None:
        await self._status(mac)
        for key in keys:
            try:
                value = self._lib.get(mac, key)
            except AttributeError:
                print(f"Invalid property {key}.")
                return
            print(f'{key} = {valueHelper.get_val(value)}')

    async def set(self, mac: str, pairs: List[List[str]]) -> None:
        await self._status(mac)
        for pair in pairs:
            key = pair[0]
            val = pair[1]

            try:
                old = self._lib.get(mac, key)
            except AttributeError:
                print(f"Invalid property {key}.")
                return

            try:
                self._lib.set(mac, key, val)
                new = self._lib.get(mac, key)
            except ValueError:
                print(f"Invalid property value {val}.")
                return

            self._send(mac)

            print(f'{key} = {valueHelper.get_val(new)} (was {valueHelper.get_val(old)})')
