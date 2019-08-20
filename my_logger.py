# -*- coding: utf-8 -*-

# from logbook import Logger, StreamHandler
import logging
import logzero
from logzero import logger


def LoggerInit():
    logzero.logfile("./logfile.log", maxBytes=10e6, backupCount=3)
    formatter = logging.Formatter(
        '%(asctime)-15s %(filename)s:%(lineno)s [%(levelname)s] %(message)s')
    logzero.formatter(formatter)


if __name__ == "__main__":
    # Setup rotating logfile with 3 rotations, each with a maximum filesize of 1MB:
    LoggerInit()
    # Log messages
    logger.info("This log message goes to the console and the logfile")
