import asyncio
import logging
from asyncio import StreamWriter, StreamReader
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST, timeout
from typing import Any, Dict

from homeeasy.CustomLogger import CustomLogger
from homeeasy.DeviceState import DeviceState

logger = CustomLogger(logging.getLogger(__name__))


class HomeEasyLibLocalDiscovery:

    @staticmethod
    def request_devices():
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(('', 2415))
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.settimeout(10)

        server_address = ('255.255.255.255', 12414)
        message = b'\xAA\xAA\x06\x02\xFF\xFF\xFF\x00\x59'

        sock.sendto(message, server_address)
        devices: Dict = dict()
        discovered = True;
        while discovered:
            try:
                data, server = sock.recvfrom(4096)
                ip = server[0]

                if data[2] == 12 and data[3] == 0x03:
                    dev_industry = data[4]
                    dev_vendor = data[5]
                    dev_type = data[6]
                    mac = data[7:12].hex()
                    if ip not in devices:
                        devices[ip] = [ip, mac, dev_industry, dev_vendor, dev_type]
                        sock.sendto(message, server_address)

            except timeout:
                discovered = False

        return devices.values()
