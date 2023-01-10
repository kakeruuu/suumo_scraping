from selenium.common.exceptions import NoSuchElementException

from log.logging import get_my_logger


def create_logging_critical(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except NoSuchElementException as e:
            logger = get_my_logger(func.__name__)
            logger.info("The specified element may not exist.")
            logger.exception("The detailed error message -", exc_info=e)

        except Exception as e:
            logger = get_my_logger(func.__name__)
            logger.info("An unexpected error has occurred.")
            logger.exception("The detailed error message -", exc_info=e)

    return wrapper
