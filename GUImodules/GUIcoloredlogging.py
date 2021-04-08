import coloredlogs, logging
import time, os

# Create a logger object.
def init_logger(__name__):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    logFile_name = 'log/'+timestr+'_ColdJigGUI.log'

    if not os.path.exists(os.path.dirname(logFile_name)):
        try:
            os.makedirs(os.path.dirname(logFile_name))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    formatter_str = "%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(threadName)s::%(message)s"
    formatter = logging.Formatter(formatter_str)


    file_handler = logging.FileHandler(logFile_name)
    file_handler.setFormatter(formatter)

    #stdout_handler = logging.StreamHandler()
    #stdout_handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    #logger.addHandler(stdout_handler)

    coloredlogs.install(level='DEBUG', logger=logger, fmt=formatter_str)


    return logger


if __name__ == '__main__':
    logger= init_logger(__name__)
    # Some examples.
    logger.debug("this is a debugging message")
    logger.info("this is an informational message")
    logger.warning("this is a warning message")
    logger.error("this is an error message")
    logger.critical("this is a critical message")
