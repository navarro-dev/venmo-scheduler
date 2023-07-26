from venmo_api import Client
import logging

def validate_vars(**kwargs):
    try:
        for k, v in kwargs.items():
            if not v or v == [''] or v == 0:
                raise ValueError(f"The {k.upper()} value is empty or not set. Add value and try again.")
    except Exception as e:
        logger.error(str(e))
        raise

def init_logger(module_name):
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
    
class Venmo():
    
    def __init__(self, access_token) -> None:
        self.client = Client(access_token=access_token)

    def send_request(self, User, amount, comment):
        try:
            self.client.payment.request_money(amount=amount, note=comment, target_user=User)
            logger.info(f"Payment request has been sent to {User.username}.")
        except Exception as e:
            logger.error(str(e))
            raise
    
    def validate_user(self, username):
        try:
            user = self.client.user.get_user_by_username(username=username)
            if user:
                logger.info(f"{user.username} user found!")
            else:
                logger.warning(f"User {username} not found. Verify username and try again.")
        except Exception as e:
            logger.error(str(e))
            raise

        return user

logger = init_logger(__name__)