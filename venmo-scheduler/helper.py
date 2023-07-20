import logging

def setup_logger(module_name):
    # create logging formatter
    logFormatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    # create console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    consoleHandler.setFormatter(logFormatter)

    # Add console handler to logger
    logger.addHandler(consoleHandler)

    return logger

# validate currency amount input
def validate_currency():
    #TODO
    print()

