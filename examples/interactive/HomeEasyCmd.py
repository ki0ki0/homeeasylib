import cmd
from structlog import get_logger

from homeeasy import valueHelper
from homeeasy.DeviceState import DeviceState
from homeeasy.HomeEasyLib import HomeEasyLib

logger = get_logger()


class HomeEasyCmd(cmd.Cmd):
    """HomeEasy HVAC command tool."""

    _mac: str
    _lib: HomeEasyLib
    _connected: bool

    def __init__(self) -> None:
        super().__init__()
        self.prompt = "HomeEasyCmd>"
        self.intro = 'HomeEasy HVAC command tool. Type "help" to get some help.'

        self._mac = ''
        self._lib = HomeEasyLib()
        self._connected = False

    def _connect(self) -> None:
        if not self._connected:
            self._connected = True
            self._lib.connect()

    def do_mac(self, mac: str) -> None:
        """mac <device mac>
            Set default mac for operations."""
        self._mac = mac

    @staticmethod
    def _print_status(mac: str, state: DeviceState) -> None:
        print(f"Status {mac}:\n{state}")

    def do_status(self, mac: str = '') -> None:
        """status [device mac]
            Dump messages from "status" queue."""
        self._connect()
        mac = mac if len(mac) != 0 else self._mac
        if len(mac) != 0:
            self._lib.dump_status(mac, self._print_status)
        else:
            self._lib.dump_status('#', self._print_status, "dev/status/")

    @staticmethod
    def _print_cmd(mac: str, state: DeviceState) -> None:
        print(f"CMD {mac}:\n{state}")

    def do_cmd(self, mac: str = '') -> None:
        """cmd [device mac]
            Dump messages from "cmd" queue."""
        self._connect()
        mac = mac if len(mac) != 0 else self._mac
        if len(mac) != 0:
            self._lib.dump_cmd(mac, self._print_cmd)
        else:
            self._lib.dump_cmd('#', self._print_cmd, "dev/cmd/")

    def do_update(self, mac: str = '') -> None:
        """update [device mac]
            Request status update for device."""
        self._connect()
        mac = mac if len(mac) != 0 else self._mac
        if len(mac) != 0:
            self._lib.request_status(mac, self._print_status)
        else:
            print("Mac is required.")

    def do_send(self, mac: str = '') -> None:
        """send [device mac]
            Get status value for device."""
        self._connect()
        mac = mac if len(mac) != 0 else self._mac
        if len(mac) == 0:
            print("Mac is required.")
            return

        self._lib.send(mac)

    def do_get(self, key: str) -> None:
        """get <key> [device mac]
            Get property value for device."""
        mac = ''
        split = key.split()
        if len(split) > 1:
            key = split[0]
            mac = split[1]

        mac = mac if len(mac) != 0 else self._mac
        if len(mac) == 0:
            print("Mac is required.")
            return

        try:
            value = self._lib.get(mac, key)
        except AttributeError:
            print(f"Invalid property {key}.")
            return

        if value is None:
            print("Device state isn't available(need update), or not valid property")
        else:
            print(f'{key} = {valueHelper.get_val(value)}')

    def do_set(self, key: str) -> None:
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

        mac = mac if len(mac) != 0 else self._mac
        if len(mac) == 0:
            print("Mac is required.")
            return

        try:
            old = self._lib.get(mac, key)
            if old is None:
                print("Device state isn't available(need update), or not valid property")
                return

            self._lib.set(mac, key, val)

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
