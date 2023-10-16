import logging

logger = logging.getLogger(__name__)
# logger.setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

# Logger configurations to write the logs to a file.
fh = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)