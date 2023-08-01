from venmo_api import User
from util import Venmo, init_logger, validate_vars, is_request_sent
import os

def run_lambda(event, context):
    main()

def main():    

    logger = init_logger(__name__)

    access_token = os.environ["ACCESS_TOKEN"]
    request_users = [u.strip() for u in os.environ["REQUEST_USERS"].split(",")]
    request_amount = float(os.environ.get("REQUEST_AMOUNT", 0))
    request_note = os.environ["REQUEST_NOTE"]
    send_request = os.environ.get("SEND_REQUEST", "FALSE").upper() == "TRUE"

    validate_vars(access_token=access_token,
                 request_users=request_users,
                 request_amount=request_amount,
                 request_note=request_note)
    logger.info("Required environment variables are set properly.")

    venmo = Venmo(access_token=access_token)
    
    logger.info("Validating user list and sending payment requests.")
    for username in request_users:
        user_found = venmo.validate_user(username)
        if user_found:
            user = User.from_json(user_found._json)

            monthly_request_sent = is_request_sent(username=user.username, 
                                                   amount=request_amount,
                                                   note=request_note,
                                                   request_list=venmo.get_charge_payments())

            if send_request and not monthly_request_sent:
                venmo.send_request(user, request_amount, request_note)

if __name__ == "__main__":
    main()