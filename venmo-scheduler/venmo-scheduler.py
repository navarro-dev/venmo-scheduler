from venmo_api import Client
from request import VRequest
from helper import setup_logger
import os

def main():    

    logger = setup_logger(__name__)

    access_token = Client.get_access_token(username=os.environ["LOGIN_EMAIL"],
                                        password=os.environ["LOGIN_PASSWORD"])
    
    username_list = [u.strip() for u in os.environ['REQUEST_USERS'].split(",")]
    request_amount = float(os.environ["REQUEST_AMOUNT"])
    request_comment = os.environ["REQUEST_COMMENT"]

    # Initialize api client
    client = Client(access_token=access_token)

    for username in username_list:
        user = VRequest(username, request_amount, request_comment, client)
        if user.validate_user():
            # user.send_request()
            print()

    client.log_out(f"Bearer {access_token}")

if __name__ == "__main__":
    main()