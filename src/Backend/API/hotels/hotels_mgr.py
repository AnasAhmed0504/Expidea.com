from ..common.reservation import ReservationManagerProcessor
from .marriot_mgr import MarriotHotelManager
from .hilton_mgr import HiltonHotelManager

class HotelManager(ReservationManagerProcessor):
    def __init__(self):
        #Creates our managers and give to parent
        mgrs = [MarriotHotelManager(), HiltonHotelManager()]
        super().__init__(mgrs)

        