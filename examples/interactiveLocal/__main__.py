import argparse
import asyncio
import logging
import sys

from examples.interactiveLocal.HomeEasyCmd import HomeEasyCmd

logging.basicConfig(
    level=logging.DEBUG
)

parser = argparse.ArgumentParser(description='HomeEasy HVAC interactive tool.')
parser.add_argument("-i", "--ip", type=str,
                    help="Set default device ip address")
parser.add_argument("-u", "--update", action='store_true',
                    help="Do update for default device at start")

args = parser.parse_args()

# For win system we have only Run mode
# For POSIX system Reader mode is preferred

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    mode = "Run"
else:
    loop = asyncio.get_event_loop()
    mode = "Reader"
# create instance
cmd = HomeEasyCmd(mode=mode)

cmd.start(loop)  # prepaire instance

if args.ip is not None:
    print(f"Device IP: {args.ip}")
    cmd.do_ip(args.ip)

if args.update:
    if args.ip is None:
        print(f"Device ip is required")
        exit(1)
    cmd.do_update()

try:
    loop.run_forever()  # our cmd will run automatilly from this moment
except KeyboardInterrupt:
    loop.stop()
