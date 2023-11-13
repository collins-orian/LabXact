#!/usr/bin/env python3
"""This module contains the logger configurations for the app"""

from logging import getLogger, FileHandler, Formatter, ERROR, INFO, DEBUG, WARNING


# Logger configurations
logger = getLogger(__name__)
# logger.setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)
logger.setLevel(ERROR)
logger.setLevel(INFO)

fh = FileHandler('app.log')
formatter = Formatter(
    '%(levelname)s - %(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
