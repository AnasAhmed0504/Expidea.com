from .payment_common import IPayment
from .stripe_external import *

class StripePayment(IPayment):
    def __init__(self):
        self.stripe = StripePaymentAPI()
        self.card = StripeCardInfo()
        self.user_info = StripeUserInfo()
    
    def set_card_info(self, id, expire_date, cvv):
        self.id = id
        self.expiry_date = expire_date
        self.cvv = cvv
    
    def set_user_info(self, name, address):
        self.name = name
        self.address = address
    
    def make_payment(self, money, user_info, card_info):
        return self.stripe.withdraw_money(money, user_info, card_info)
    
    def cancel_payment(self, transaction_id):
        return self.stripe.cancel_money(transaction_id)