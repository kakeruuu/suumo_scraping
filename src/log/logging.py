import os
import pathlib
import logging


def get_my_logger(name: str):
    
    if not(os.path.isdir("./log")):
        os.makedirs("./log")
        log_path = pathlib.Path("./log/process.log")
        log_path.touch()

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler("./log/process.log")
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(name)s - %(message)s")

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

if __name__ == "__main__":
    get_my_logger()