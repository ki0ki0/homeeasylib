import argparse
import logging
import structlog
from HomeEasyCmd import HomeEasyCmd

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO
    )
    structlog.configure(
        processors=[
            structlog.processors.KeyValueRenderer(
                key_order=["topic"]
            )
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    parser = argparse.ArgumentParser(description='HomeEasy HVAC command tool.')
    parser.add_argument("-v", "--verbosity", nargs='?', type=str, choices=["None", "Info", "Debug"],
                        const='Info', default='None',
                        help="Set output verbosity")
    parser.add_argument("-m", "--mac", type=str,
                        help="Set default device mac address")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--update", action='store_true',
                       help="Do update for default device at start")
    group.add_argument("-g", "--get", type=str, nargs='+', metavar='property',
                       help="Get value of device state property")
    group.add_argument("-s", "--set", type=tuple, nargs=2, action="extend",
                       metavar=('property', 'value'),
                       help="Get value of device state property")

    args = parser.parse_args()

    cmd = HomeEasyCmd()

    if args.mac is not None:
        print(f"Device mac: {args.mac}")
        cmd.do_mac(args.mac)

    if args.get is not None or args.get is not None:
        if args.mac is None:
            print(f"Device mac is required")
            exit(1)
        cmd.do_update('')
        exit(0)

    if args.update:
        print(f"Device update is requested")
        cmd.do_update('')

    cmd.cmdloop()
