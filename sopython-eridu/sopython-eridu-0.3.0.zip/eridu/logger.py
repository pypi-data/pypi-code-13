import logging

logger = logging.getLogger('eridu')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(ch)
