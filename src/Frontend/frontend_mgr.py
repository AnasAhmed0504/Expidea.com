from .customer_frontend_mgr import CustomerFrontendManager
from ..Backend.user import Customer
from .siteaccess_mgr import SiteAccessManager

class FrontendManager:
    def __init__(self):
        self.access_site = SiteAccessManager()

    def run(self):
        while True:
            try:
                user = self.access_site.get_accessed_user()

                if isinstance(user, Customer):
                    CustomerFrontendManager(user).run()
                else: 
                    raise NotImplemented
            
            except BaseException as e:
                print(e)
                raise e

