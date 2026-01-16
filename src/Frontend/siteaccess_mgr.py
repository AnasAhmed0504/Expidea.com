from .utils import get_menu_choice
from ..Backend.user_mgr import UsersManager

class SiteAccessManager:
    def __init__(self):
        self.users_mgr = UsersManager()

    def print_menu(self):
        return get_menu_choice("Sysems Access", ["Login", "Sign up", "Exit"])
    
    def get_accessed_user(self):
        funcs = [self.login, self.signup]

        while True:
            choice = self.print_menu()
            
            if choice == 3:  # Exit option
                print("Thank you for using Expedia! Goodbye!")
                return None
            
            user = funcs[choice-1]()

            if user is not None:
                return user
            else:
                print("Try again")

    def login(self):
        username = input('Enter username: ')
        password = input('Enter password: ')

        user = self.users_mgr.get_user(username, password)
        if user is None:
            print("\nInvalid username or password")
        return user
    
    def signup(self):
        username = input('Enter username: ')
        password = input('Enter password: ')
        name = input('Enter full name: ')
        email = input('Enter email: ')
        
        user = self.users_mgr.register_user(username, password, name, email)
        if user is None:
            print("\nUsername already exists or registration failed")
        return user
