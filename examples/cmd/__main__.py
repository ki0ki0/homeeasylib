import argparse
import asyncio
import logging
import sys


from examples.cmd.HomeEasy import HomeEasy
from homeeasy.HomeEasyLibLocalDiscovery import HomeEasyLibLocalDiscovery

logging.basicConfig(
    level=logging.DEBUG
)


async def main():
    parser = argparse.ArgumentParser(description='HomeEasy HVAC command tool.')

    parser.add_argument("-d", "--discover", action='store_false',
                        help="Discover available devices")

    parser.add_argument("-i", "--ip", type=str,
                        help="Set device ip address")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--get", type=str, nargs='+', metavar='property',
                       help="Get value of device state property")
    group.add_argument("-s", "--set", type=str, nargs=2, action="append",
                       metavar=('property', 'value'),
                       help="Get value of device state property")

    args = parser.parse_args()

    cmd = HomeEasy()

    if args.discover is False:
        discovery = HomeEasyLibLocalDiscovery()
        devices = discovery.request_devices()
        print("Available devices: " + str(list(map(lambda d: {d[0], d[1]}, devices))))
        exit(1)

    if args.ip is None:
        print(f"Device ip is required")
        exit(1)

    print(f"Device ip: {args.ip}")

    if args.get is not None:
        await cmd.get(args.ip, args.get)
    elif args.set is not None:
        await cmd.set(args.ip, args.set)
    else:
        await cmd.status(args.ip)


loop = asyncio.ProactorEventLoop()
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
