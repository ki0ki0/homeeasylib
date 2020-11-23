import argparse
import asyncio
import logging
import sys


from examples.cmd.HomeEasy import HomeEasy

logging.basicConfig(
    level=logging.DEBUG
)


async def main():
    parser = argparse.ArgumentParser(description='HomeEasy HVAC command tool.')

    parser.add_argument("-m", "--mac", type=str, required=True,
                        help="Set default device mac address")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--get", type=str, nargs='+', metavar='property',
                       help="Get value of device state property")
    group.add_argument("-s", "--set", type=str, nargs=2, action="append",
                       metavar=('property', 'value'),
                       help="Get value of device state property")

    args = parser.parse_args()

    cmd = HomeEasy()

    if args.mac is None:
        print(f"Device mac is required")
        exit(1)

    print(f"Device mac: {args.mac}")

    if args.get is not None:
        await cmd.get(args.mac, args.get)
    elif args.set is not None:
        await cmd.set(args.mac, args.set)
    else:
        await cmd.status(args.mac)


loop = asyncio.ProactorEventLoop()
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
