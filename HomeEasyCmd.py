import cmd
from typing import Any

from structlog import get_logger

from HomeEasyLib import HomeEasyLib


logger = get_logger()


class HomeEasyCmd(cmd.Cmd):
    """HomeEasy HVAC command tool."""

    lib: HomeEasyLib
    mac: str

    def do_mac(self, mac: str):
        """mac [device mac]
            Set default mac for operations."""
        self.mac = mac

    def do_status(self, mac: str):
        """status [device mac]
            Dump messages from "status" queue."""
        mac = mac if len(mac) != 0 else self.mac
        if len(mac) != 0:
            self.lib.dump_status(mac)
        else:
            self.lib.dump_status('#', "dev/status/")

    def do_cmd(self, mac: str):
        """cmd [device mac]
            Dump messages from "cmd" queue."""
        mac = mac if len(mac) != 0 else self.mac
        if len(mac) != 0:
            self.lib.dump_cmd(mac)
        else:
            self.lib.dump_cmd('#', "dev/cmd/")

    def do_update(self, mac: str):
        """update [device mac]
            Request status update for device."""
        mac = mac if len(mac) != 0 else self.mac
        if len(mac) != 0:
            self.lib.request_status(mac)
        else:
            print("Mac is required.")

    def do_send(self, mac: str = ''):
        """send [device mac]
            Get status value for device."""
        mac = mac if len(mac) != 0 else self.mac
        if len(mac) == 0:
            print("Mac is required.")
            return

        self.lib.send(mac)

    def do_get(self, key: str, mac: str = ''):
        """get <key> [device mac]
            Get status value for device."""
        mac = mac if len(mac) != 0 else self.mac
        if len(mac) == 0:
            print("Mac is required.")
            return

        value = self.lib.get(mac, key)
        if value is None:
            print("Device state isn't available(need update), or not valid property")
        else:
            print(f"{mac} {key}={value}")

    def do_set(self, key: str, value: Any = True, mac: str = ''):
        """update <device mac>
            Set status value for device."""
        mac = mac if len(mac) != 0 else self.mac
        if len(mac) == 0:
            print("Mac is required.")
            return

        old = self.lib.get(mac, key)
        if old is None:
            print("Device state isn't available(need update), or not valid property")
            return

        self.lib.set(mac, key, value)

    # noinspection PyMethodMayBeStatic
    def do_exit(self):
        """exit
            Close the tool."""
        exit(0)

    # noinspection PyPep8Naming, PyMethodMayBeStatic
    def do_EOF(self):
        return True

    def preloop(self) -> None:
        self.lib = HomeEasyLib()
        self.lib.connect()
        self.prompt = "HomeEasyCmd>"
        self.intro = 'HomeEasy HVAC command tool. Type "help" to get some help.'
        super().preloop()

    def postloop(self) -> None:
        self.lib.disconnect()
        super().postloop()
