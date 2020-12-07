import argparse
import logging
from examples.interactive.HomeEasyCmd import HomeEasyCmd

logging.basicConfig(
    level=logging.DEBUG
)


def main() -> None:
    parser = argparse.ArgumentParser(description='HomeEasy HVAC interactive tool.')
    parser.add_argument("-m", "--mac", type=str,
                        help="Set default device mac address")
    parser.add_argument("-u", "--update", action='store_true',
                        help="Do update for default device at start")

    args = parser.parse_args()

    cmd = HomeEasyCmd()

    if args.mac is not None:
        print(f"Device mac: {args.mac}")
        cmd.do_mac(args.mac)

    if args.update:
        if args.mac is None:
            print(f"Device mac is required")
            exit(1)
        cmd.do_update('')

    cmd.cmdloop()


main()
