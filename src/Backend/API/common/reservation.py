from abc import ABC, abstractmethod

class IReservation(ABC):
    @property
    @abstractmethod
    def total_cost(self):
        pass

    @property
    @abstractmethod
    def mgr(self): # The (flight/hotel) manager that is responsible for reserve/cancel this reservarion
        # also maintaining it as a property, so if I later wanted  to reserve or cancel it
        #this makes the code much more simpler
        pass

    @abstractmethod
    def __repr__(self):
        pass


class ItineraryReservation(IReservation):
    """
    Itenerary reservation is just a collection of reservarions so follows same interface
    """
    def __init__(self):
        super().__init__()
        self.reservations = []

    @property
    def total_cost(self):
        return sum([reservation.total_cost for reservation in self.reservations])
    
    @property
    def mgr(self):
        return None #Each internal reservation has its own manager
    
    def __repr__(self):
        res = f"Itenerary Total Cost {self.total_cost}\n\t" + \
                "\n\t".join(repr(reservation) for reservation in self.reservations)
        return res
    
class IReservationManager(ABC):
    """
    This is going to be the common interface between aircanada and turkish airlines APIs
    1. we need to search for available flights/hotels
    2. we need to reserve a flight/hotel
    3. we need to cancel a reservation
    """
    @abstractmethod
    def search(self, request):
        pass

    @abstractmethod
    def reserve(self, reservation: IReservation):
        pass

    @abstractmethod
    def cancel(self, reservation: IReservation):
        pass


class ReservationManagerProcessor(IReservationManager):
    """
    Respresents a group of (flight/hotel) managers
    This class has all the managers
    """
    def __init__(self, mgrs):
        super().__init__()    
        self.mgrs = mgrs

    def search(self, request):
        #the search request is asking all of them to search
        # then aggregate all the results
        aggregated_results = []

        for mgr in self.mgrs:
            aggregated_results.extend(mgr.search(request))

        return aggregated_results
    
    def reserve(self, reservation: IReservation):
        # The reserve is asking for a specific manager to reserve
        return reservation.mgr.reserve(reservation) 
    
    def cancel(self, reservation: IReservation):
        #The cancel is asking for a specific manager to make the cancellation
        return reservation.mgr.cancel(reservation) 