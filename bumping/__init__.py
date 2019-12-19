import logging

__version__ = '0.5.1'


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def set_debug(debug):
    global logger
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
