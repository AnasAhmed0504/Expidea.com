class User:
    def __init__(self, user_name, password, name, email):
        self.user_name = user_name
        self.password = password
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Welcome {self.name} | {type(self).__name__}"
    # the part of type(self).__name__
    # This is useful for polymorphic behavior—the same method displays different class names 
    # depending on which subclass the object is an instance of.


class Customer(User):
    def __init__(self, user_name, password, name, email):
        super().__init__(user_name, password, name, email)
        self.payment_cards = []

class Admin(User):
    pass