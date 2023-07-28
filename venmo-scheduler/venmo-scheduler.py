from venmo_api import User
from util import Venmo, init_logger, validate_vars
import os

def run_lambda(event, context):
    main()

def main():    

    logger = init_logger(__name__)

    access_token = os.environ["ACCESS_TOKEN"]
    request_users = [u.strip() for u in os.environ["REQUEST_USERS"].split(",")]
    request_amount = float(os.environ.get("REQUEST_AMOUNT", 0))
    request_comment = os.environ["REQUEST_COMMENT"]
    send_request = os.environ.get("SEND_REQUEST", "FALSE").upper() == "TRUE"

    validate_vars(access_token=access_token,
                 request_users=request_users,
                 request_amount=request_amount)
    logger.info("Required environment variables are set properly.")

    venmo = Venmo(access_token=access_token)
    
    logger.info("Validating user list and sending payment requests.")
    for username in request_users:
        user_found = venmo.validate_user(username)
        if user_found:
            user = User.from_json(user_found._json)
            if send_request:
                venmo.send_request(user, request_amount, request_comment)

if __name__ == "__main__":
    main()