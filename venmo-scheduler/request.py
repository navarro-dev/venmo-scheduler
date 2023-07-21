from helper import init_logger

logger = init_logger(__name__)

class VRequest():

    def __init__(self, username, amount, comment, client, id=None) -> None:
        self.username = username
        self.amount = float(amount)
        self.comment = comment
        self.client = client
        self.id = id

    def send_request(self):
        self.client.payment.request_money(self.amount, self.comment, self.id)
        logger.info(f"Payment request has been sent to {self.username}.")
    
    def validate_user(self):
        search = self.client.user.search_for_users(query=f"{self.username}")
        if search:
            for user in search:
                if (user.username).lower() == (self.username).lower():
                    self.set_id(user.id)
                    logger.info(f"{user.username} user found!")
                    return True
        else:
            logger.warning(f"User {self.username} not found. Verify username and try again.")

        return False
    
    def set_id(self, id):
        self.id = id
    
    def __str__(self) -> str:
        return self.username
    