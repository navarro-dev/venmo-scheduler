from venmo_api import Client
from datetime import datetime
import logging
import os

def is_request_sent(username, amount, request_list):

    for request in request_list:

        request_date = datetime.fromtimestamp(request.date_created)
        today = datetime.now()

        if (request.target.username == username and 
                float(request.amount) == amount and
                month_year_date(request_date) == month_year_date(today)):
            logger.info(f"Payment request has already been sent to {username} this month.")
            return True
        else:
            return False
            

def month_year_date(date):
    return date.strftime("%B %d %Y")

def validate_vars(**kwargs):
    try:
        for k, v in kwargs.items():
            if not v or v == [''] or v == 0:
                raise ValueError(f"The {k.upper()} value is empty or not set. Add value and try again.")
    except Exception as e:
        logger.error(str(e))
        raise

def init_logger(module_name):
    
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    # create handler only if application runs outside AWS Lambda, Lambda uses it's own handler
    if "LAMBDA_TASK_ROOT" not in os.environ:
        # create logging formatter and console handler for local dev
        logFormatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(logFormatter)

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
    
    def get_charge_payments(self):
        try:
            return self.client.payment.get_charge_payments()
        except Exception as e:
            logger.error(str(e))
            raise

logger = init_logger(__name__)