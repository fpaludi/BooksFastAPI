import logging
import sys
from logging.handlers import TimedRotatingFileHandler


class LoggerBuilder:

    _LOG_TYPE_MAPPER = {
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "error": logging.ERROR,
        "warning": logging.WARNING,
    }

    _DEFAULT_FORMATTER = logging.Formatter(
        "[%(asctime)s — %(filename)s:%(lineno)s — %(funcName)s() — %(levelname)s] %(message)s"
    )

    def __init__(
        self,
        module,
        log_type="info",
        format_str="",
        use_file=False,
        log_file_name="my_app.log",
    ):

        self._log_type = self._LOG_TYPE_MAPPER[log_type]
        self._file_name = log_file_name
        self._format = format_str
        if format_str == "":
            self._format = self._DEFAULT_FORMATTER
        self._logger = logging.getLogger(module)
        self._logger.setLevel(
            logging.INFO
        )  # better to have too much log than not enough
        self._logger.addHandler(self._get_console_handler())
        if use_file:
            self._logger.addHandler(self._get_file_handler())
        self._logger.propagate = False

    def _get_console_handler(self):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self._format)
        return handler

    def _get_file_handler(self):
        handler = TimedRotatingFileHandler(self._file_name, when="midnight")
        handler.setFormatter(self._format)
        return handler

    def get_logger(self):
        return self._logger
