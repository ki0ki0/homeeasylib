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

    HomeEasyCmd().cmdloop()
