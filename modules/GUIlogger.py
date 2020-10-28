#--Setup logging
import logging
import time, os

def init_logger(__name__):
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(threadName)s::%(message)s")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    logFile_name = 'log/'+timestr+'_ColdJigGUI.log'

    if not os.path.exists(os.path.dirname(logFile_name)):
        try:
            os.makedirs(os.path.dirname(logFile_name))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    file_handler = logging.FileHandler(logFile_name)
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)


    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    return logger
