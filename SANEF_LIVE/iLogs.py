import time
import logging
import logging.handlers

def iLog(message):
    path ='D://Daily_backup//sanef_Logs_Test.log'
    log_handler = logging.handlers.TimedRotatingFileHandler(path, when="h",  interval=12, backupCount=1)
    formatter = logging.Formatter("%(asctime)s %(message)s")
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)
    logging.info(message)
    return True
