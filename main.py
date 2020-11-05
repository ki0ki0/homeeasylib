import logging
import sys
import time

import structlog

from HomeEasyLib import HomeEasyLib

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO
    )
    structlog.configure(
         logger_factory=structlog.stdlib.LoggerFactory(),
    )

    mac = sys.argv[1] if len(sys.argv) > 1 else None

    lib = HomeEasyLib()
    if mac is not None:
        lib.receive(mac)
        lib.request_status(mac)
    else:
        lib.receive('#', "dev/status/")

    time.sleep(60)
    lib.stop()
