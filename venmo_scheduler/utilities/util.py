from datetime import datetime

from venmo_api import PaymentStatus
from utilities.logger import set_logger

logger = set_logger("VenmoScheduler")

def is_request_sent(username, amount, note, request_list) -> bool:

    for request in request_list:
        request_date = datetime.fromtimestamp(request.date_created)
        today = datetime.now()

        if (request.target.username == username and 
                float(request.amount) == amount and
                request.status != PaymentStatus.CANCELLED and
                request.note == note and
                month_year_date(request_date) == month_year_date(today)):
            
            logger.warning(f"Payment request has already been sent to {username} this month.")
            return True
        
    return False

def month_year_date(date) -> str:
    return date.strftime("%B %Y")

