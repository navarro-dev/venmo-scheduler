from venmo_api import Client
from request import VRequest
from helper import init_logger, validate_vars
import os

def main():    

    logger = init_logger(__name__)

    login_email = os.environ["LOGIN_EMAIL"]
    login_password = os.environ["LOGIN_PASSWORD"]
    request_users = [u.strip() for u in os.environ["REQUEST_USERS"].split(",")]
    request_amount = os.environ.get("REQUEST_AMOUNT", 0)
    request_comment = os.environ["REQUEST_COMMENT"]
    send_request = os.environ.get("SEND_REQUEST", "FALSE").upper() == "TRUE"

    validate_vars(login_email=login_email,
                 login_password=login_password,
                 request_users=request_users,
                 request_amount=request_amount)

    try:
        access_token = Client.get_access_token(username=login_email,
                                            password=login_password)
    except Exception as e:
        logger.error(str(e))
        raise

    # Initialize api client
    client = Client(access_token=access_token)
    
    for username in request_users:
        user = VRequest(username, request_amount, request_comment, client)
        if user.validate_user():
            if send_request:
                user.send_request()

    client.log_out(f"Bearer {access_token}")

if __name__ == "__main__":
    main()