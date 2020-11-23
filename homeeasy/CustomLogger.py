from logging import Logger


class CustomLogger():

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self._logger = logger

    # noinspection PyMethodMayBeStatic
    def _extend_message(self, kwargs, msg):
        if len(kwargs) != 0:
            data_msg = str(kwargs)
            msg = msg + f"({data_msg})"
        return msg

    def debug(self, msg, *args, **kwargs) -> None:
        msg = self._extend_message(kwargs, msg)
        self._logger.debug(msg, *args, extra=kwargs)

    def info(self, msg, *args, **kwargs) -> None:
        msg = self._extend_message(kwargs, msg)
        self._logger.info(msg, *args, extra=kwargs)

    def warning(self, msg, *args, **kwargs) -> None:
        msg = self._extend_message(kwargs, msg)
        self._logger.warning(msg, *args, extra=kwargs)

    def warn(self, msg, *args, **kwargs) -> None:
        msg = self._extend_message(kwargs, msg)
        self._logger.warn(msg, *args, extra=kwargs)

    def error(self, msg, *args, **kwargs) -> None:
        msg = self._extend_message(kwargs, msg)
        self._logger.error(msg, *args, extra=kwargs)

    def exception(self, msg, *args, **kwargs) -> None:
        msg = self._extend_message(kwargs, msg)
        self._logger.exception(msg, *args, extra=kwargs)

    def critical(self, msg, *args, **kwargs) -> None:
        msg = self._extend_message(kwargs, msg)
        self._logger.critical(msg, *args, extra=kwargs)

    def log(self, level, msg, *args, **kwargs) -> None:
        msg = self._extend_message(kwargs, msg)
        self._logger.log(level, msg, *args,  extra=kwargs)
