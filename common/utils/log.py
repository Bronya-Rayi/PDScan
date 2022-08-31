import logging
import config

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)
handler = logging.FileHandler(config.ASSIGN_TASKS_LOG_PATH, encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',"%m-%d-%H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)