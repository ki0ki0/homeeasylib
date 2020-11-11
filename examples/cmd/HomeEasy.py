from typing import List

from structlog import get_logger

from HomeEasyLib import valueHelper
from HomeEasyLib.HomeEasyLib import HomeEasyLib, DeviceState

logger = get_logger()


class HomeEasy:

    lib: HomeEasyLib

    def __init__(self) -> None:
        self.lib = HomeEasyLib()

    async def _status(self, mac: str) -> DeviceState:
        self.lib.connect()
        return await self.lib.request_status_async(mac)

    def _send(self, mac: str) -> None:
        self.lib.send(mac)

    async def status(self, mac: str) -> None:
        status = await self._status(mac)
        print(f"{status}")

    async def get(self, mac: str, keys: List[str]) -> None:
        await self._status(mac)
        for key in keys:
            try:
                value = self.lib.get(mac, key)
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
                old = self.lib.get(mac, key)
            except AttributeError:
                print(f"Invalid property {key}.")
                return

            try:
                self.lib.set(mac, key, val)
                new = self.lib.get(mac, key)
            except ValueError:
                print(f"Invalid property value {val}.")
                return

            self._send(mac)

            print(f'{key} = {valueHelper.get_val(new)} (was {valueHelper.get_val(old)})')


