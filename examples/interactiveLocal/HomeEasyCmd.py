import asyncio

import logging

from asynccmd import Cmd

from homeeasy import valueHelper
from homeeasy.CustomLogger import CustomLogger
from homeeasy.DeviceState import DeviceState
from homeeasy.HomeEasyLib import HomeEasyLib
from homeeasy.HomeEasyLibLocal import HomeEasyLibLocal

logger = CustomLogger(logging.getLogger(__name__))


class HomeEasyCmd(Cmd):
    """HomeEasy HVAC command tool."""

    _ip: str
    _lib: HomeEasyLibLocal
    _connected: bool

    def __init__(self, mode="Reader") -> None:
        super().__init__(mode)
        self.prompt = "HomeEasyCmd>"
        self.intro = 'HomeEasy HVAC command tool. Type "help" to get some help.'

        self._ip = ''
        self._lib = HomeEasyLibLocal()
        self._connected = False

    def start(self, loop=None):
        # We pass our loop to Cmd class.
        # If None it try to get default asyncio loop.
        self.loop = loop
        # Create async tasks to run in loop. There is run_loop=false by default
        super().cmdloop(loop)

    async def _connect(self, ip: str) -> None:
        if not self._connected:
            self._connected = True
            await self._lib.connect(ip)

    def do_ip(self, ip: str) -> None:
        """ip <device ip>
            Set default ip for operations."""
        self._ip = ip

    @staticmethod
    def _print_status(ip: str, state: DeviceState) -> None:
        print(f"Status {ip}:\n{state}")

    @staticmethod
    def _print_cmd(ip: str, state: DeviceState) -> None:
        print(f"CMD {ip}:\n{state}")

    def do_update(self, ip: str = '') -> None:
        """update [device ip]
            Request status update for device."""
        ip = ip if len(ip) != 0 else self._ip
        if len(ip) != 0:
            self.loop.create_task(self._update(ip))
        else:
            print("IP is required.")

    async def _update(self, ip: str):
        await self._connect(ip)
        state = await self._lib.request_status_async()
        self._print_status(ip, state)

    def do_send(self, ip: str = '') -> None:
        """send [device ip]
            Get status value for device."""
        ip = ip if len(ip) != 0 else self._ip
        if len(ip) == 0:
            print("IP is required.")
            return

        self.loop.create_task(self._send(ip))

    async def _send(self, ip: str):
        await self._connect(ip)
        await self._lib.send()

    def do_get(self, key: str) -> None:
        """get <key>
            Get property value for device."""
        try:
            value = self._lib.get(key)
        except AttributeError:
            print(f"Invalid property {key}.")
            return

        if value is None:
            print("Device state isn't available(need update), or not valid property")
        else:
            print(f'{key} = {valueHelper.get_val(value)}')

    def do_set(self, key: str) -> None:
        """set <key> <value>
            Set property value for device."""
        split = key.split()
        if len(split) == 1:
            print("Value is required.")
            return
        key = split[0]
        val = split[1]

        try:
            old = self._lib.get(key)
            if old is None:
                print("Device state isn't available(need update), or not valid property")
                return

            self._lib.set(key, val)

            self.do_get(key)
        except AttributeError:
            print(f"Invalid property {key}.")
        except ValueError:
            print(f"Invalid property value {val}.")

    # noinspection PyMethodMayBeStatic
    def do_exit(self, _line: str) -> None:
        """exit
            Close the tool."""
        exit(0)

    # noinspection PyPep8Naming
    def do_EOF(self, _line: str) -> bool:
        self._lib.disconnect()
        return True
