import cmd
from structlog import get_logger

import valueHelper
from HomeEasyLib import HomeEasyLib


logger = get_logger()


class HomeEasyCmd(cmd.Cmd):
    """HomeEasy HVAC command tool."""

    lib: HomeEasyLib
    mac: str = ''
    lib = HomeEasyLib()
    prompt = "HomeEasyCmd>"
    intro = 'HomeEasy HVAC command tool. Type "help" to get some help.'
    connected: bool = False

    def _connect(self):
        if not self.connected:
            self.lib.connect()

    def do_mac(self, mac: str):
        """mac <device mac>
            Set default mac for operations."""
        self.mac = mac

    def do_status(self, mac: str = ''):
        """status [device mac]
            Dump messages from "status" queue."""
        self._connect()
        mac = mac if len(mac) != 0 else self.mac
        if len(mac) != 0:
            self.lib.dump_status(mac)
        else:
            self.lib.dump_status('#', "dev/status/")

    def do_cmd(self, mac: str = ''):
        """cmd [device mac]
            Dump messages from "cmd" queue."""
        self._connect()
        mac = mac if len(mac) != 0 else self.mac
        if len(mac) != 0:
            self.lib.dump_cmd(mac)
        else:
            self.lib.dump_cmd('#', "dev/cmd/")

    async def do_update(self, mac: str = ''):
        """update [device mac]
            Request status update for device."""
        self._connect()
        mac = mac if len(mac) != 0 else self.mac
        if len(mac) != 0:
            state = await self.lib.request_status(mac)
            print(f"{mac}:\n{state}")
        else:
            print("Mac is required.")

    async def do_send(self, mac: str = ''):
        """send [device mac]
            Get status value for device."""
        # await self._connect()
        mac = mac if len(mac) != 0 else self.mac
        if len(mac) == 0:
            print("Mac is required.")
            return

        self.lib.send(mac)

    def do_get(self, key: str):
        """get <key> [device mac]
            Get property value for device."""
        mac = ''
        split = key.split()
        if len(split) > 1:
            key = split[0]
            mac = split[1]

        mac = mac if len(mac) != 0 else self.mac
        if len(mac) == 0:
            print("Mac is required.")
            return

        try:
            value = self.lib.get(mac, key)
        except AttributeError:
            print(f"Invalid property {key}.")
            return

        if value is None:
            print("Device state isn't available(need update), or not valid property")
        else:
            print(f'{key} = {valueHelper.get_val(value)}')

    def do_set(self, key: str):
        """set <key> <value> [device mac]
            Set property value for device."""
        split = key.split()
        if len(split) == 1:
            print("Value is required.")
            return
        key = split[0]
        val = split[1]
        mac = ''

        if len(split) > 2:
            mac = split[2]

        mac = mac if len(mac) != 0 else self.mac
        if len(mac) == 0:
            print("Mac is required.")
            return

        try:
            old = self.lib.get(mac, key)
            if old is None:
                print("Device state isn't available(need update), or not valid property")
                return

            self.lib.set(mac, key, val)

            self.do_get(key)
        except AttributeError:
            print(f"Invalid property {key}.")
        except ValueError:
            print(f"Invalid property value {val}.")

    # noinspection PyMethodMayBeStatic
    def do_exit(self, _line: str):
        """exit
            Close the tool."""
        exit(0)

    # noinspection PyPep8Naming, PyMethodMayBeStatic
    def do_EOF(self, _line: str):
        self.lib.disconnect()
        return True
