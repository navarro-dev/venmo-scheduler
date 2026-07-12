from utilities.util import is_request_sent
from utilities.venmo import Venmo
from utilities.logger import set_logger
import os

logger = set_logger("VenmoScheduler")

def run_lambda(event, context):
    return main()

def main():

    access_token = os.environ.get("ACCESS_TOKEN", "")
    request_users = [u.strip() for u in os.environ.get("REQUEST_USERS", "").split(",") if u.strip()]
    request_amount = float(os.environ.get("REQUEST_AMOUNT", 0))
    request_note = os.environ.get("REQUEST_NOTE", "")
    send_request = os.environ.get("SEND_REQUEST", "FALSE").upper() == "TRUE"

    if not access_token:
        logger.error("ACCESS_TOKEN is not set.")
        return {"statusCode": 400, "body": "ACCESS_TOKEN is not set."}
    if not request_note:
        logger.error("REQUEST_NOTE is not set.")
        return {"statusCode": 400, "body": "REQUEST_NOTE is not set."}
    if request_amount == 0:
        logger.error("REQUEST_AMOUNT is not set or is zero.")
        return {"statusCode": 400, "body": "REQUEST_AMOUNT is not set or is zero."}
    if not request_users:
        logger.warning("REQUEST_USERS is empty.")
        return {"statusCode": 400, "body": "REQUEST_USERS is empty."}

    logger.info("Starting payment request process...")
    try:
        venmo_client = Venmo(access_token=access_token)
    except Exception as e:
        logger.error(f"Error initializing Venmo client: {str(e)}")
        raise

    charge_payments = venmo_client._get_charge_payments()

    for username in request_users:
        try:
            user = venmo_client._validate_user(username)

            if user:
                logger.info(f"{user.username} user found!")
                monthly_request_sent = is_request_sent(username=user.username,
                                                    amount=request_amount,
                                                    note=request_note,
                                                    request_list=charge_payments)

                if send_request and not monthly_request_sent:
                    venmo_client._send_request(user, request_amount, request_note)
                    logger.info(f"Payment request has been sent to {user.username}.")
                elif not send_request:
                    logger.info(f"SEND_REQUEST is set to {send_request}, therefore no payment request was sent.")

        except Exception as e:
            logger.error(f"Error processing payment request to user {username}: {str(e)}")
            continue

    return {
        "statusCode": 200,
        "body": "Payment request process completed."
    }

if __name__ == "__main__":
    main()