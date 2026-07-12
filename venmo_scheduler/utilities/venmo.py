
from venmo_api import Client, User, Page
from utilities.logger import set_logger

logger = set_logger("VenmoScheduler")

def generate_access_token(username, password):
    try:
        access_token = Client.get_access_token(username=username, password=password)
        logger.info("Access token generated successfully.")
        return access_token
    except Exception as e:
        logger.error(str(e))
        raise

class Venmo():
    
    def __init__(self, access_token) -> None:
        self.client = Client(access_token=access_token)

    def _send_request(self, User, amount, note) -> bool:
        return self.client.payment.request_money(amount=amount, note=note, target_user=User)  
    
    def _validate_user(self, username) -> User:    
        return self.client.user.get_user_by_username(username=username)
    
    def _get_charge_payments(self) -> Page:
        return self.client.payment.get_charge_payments()
