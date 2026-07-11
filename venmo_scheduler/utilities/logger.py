import logging
import os

_FORMMATTED_LOGGERS: set[str] = set()

def set_logger(logger_name: str) -> logging.Logger:
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # avoids attaching multiple handlers to the same logger, preventing duplicate log messages
    if logger_name in _FORMMATTED_LOGGERS:
        return logger

    _FORMMATTED_LOGGERS.add(logger_name)

    logger.propagate = False

    # create handler only if application runs outside AWS Lambda, Lambda uses it's own handler
    if "LAMBDA_TASK_ROOT" not in os.environ:
        # create logging formatter and console handler for local dev
        logFormatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(logFormatter)

        logger.addHandler(consoleHandler)
    

    return logger