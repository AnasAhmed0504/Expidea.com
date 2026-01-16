from ..common.reservation import ReservationManagerProcessor
from .aircanada_mgr import AirCanadaManager
from .turkish_mgr import TurkishAirlinesManager

class FlightManager(ReservationManagerProcessor):
    #extends from the reservation manager processor
    def __init__(self):
        # the usage of that mainly is to aggregate multiiple managers
        # so if we have a new manager we just add it here
        mgrs = [AirCanadaManager(), TurkishAirlinesManager()]

        super().__init__(mgrs)