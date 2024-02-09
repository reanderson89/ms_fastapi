# This is a custom logging format for the SQS queue consumers and producers.

import logging
from colorlog import ColoredFormatter

GSDPROD_LEVEL = 25
YASS_LEVEL = 35
MILESTONE_LEVEL = 45

logging.addLevelName(GSDPROD_LEVEL, "GSDPROD")
logging.addLevelName(YASS_LEVEL, "YASS")
logging.addLevelName(MILESTONE_LEVEL, "MILESTONE")

class CustomLogger(logging.Logger):
    """Custom logger class with multiple `log` methods."""
    def gsd_producer(self, message, *args, **kws):
        """Log 'message % args' with severity 'GSDPROD'."""
        self._log(GSDPROD_LEVEL, message, args, **kws)

    def yass(self, message, *args, **kws):
        """Log 'message % args' with severity 'YASS'."""
        self._log(YASS_LEVEL, message, args, **kws)

    def milestone(self, message, *args, **kws):
        """Log 'message % args' with severity 'MILESTONE'."""
        self._log(MILESTONE_LEVEL, message, args, **kws)
# def gsd_producer(self, message, *args, **kws):
#     self._log(GSDPROD_LEVEL, message, args, **kws)


# def yass(self, message, *args, **kws):
#     self._log(YASS_LEVEL, message, args, **kws)


# def milestone(self, message, *args, **kws):
#     self._log(MILESTONE_LEVEL, message, args, **kws)


# logging.Logger.gsd_producer = gsdprod
# logging.Logger.yass = yass
# logging.Logger.milestone = milestone


def init_logger(worker_name: str = None):
    """Initialize logger with custom logging format."""

    logger = CustomLogger(__name__)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    worker_id = worker_name if worker_name else "worker %(process)d"
    formatter = ColoredFormatter(
        f"%(log_color)s[%(levelname)s- {worker_id}]%(reset)s %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "purple",
            "INFO": "green",
            "GSDPROD": "purple",
            "YASS": "bold_blue",
            "MILESTONE": "bold_cyan",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        }
    )

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
