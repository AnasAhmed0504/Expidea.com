from .aircanada_external import AirCanadaOnlineAPI, AirCanadaFlight, AirCanadaCustomerInfo
from .flight_common import Flight, FlightRequest, FlightReservation
from ..common.reservation import IReservationManager
from ..common.customer_info import CustomerInfo

class AirCanadaManager(IReservationManager):
    """
    Aircanada external API allows to search/reserve/cancel flights
    So we need to have our own class that doesn't depend directly on the external API
    So this aircanada manager is created to do that job

    It is extending from the interface reservation manager
    it does the search/reserve/cancel methods

    """
    def __init__(self):
        pass

    def search(self, request):
        # I start to contact theair canada api with the get_flights method
        # and give all the information it needs (which actually exists) from the request
        flights_external = AirCanadaOnlineAPI.get_flights(request.from_loc, request.datetime_from,
                                        request.to_loc, request.datetime_to,
                                        request.adults, request.children, request.infants)
        # Convert from external API format to internal format
        flights = []
        for flight_external in flights_external:
            # so we take all what we need and create our own flight object
            # self represents the manager that created this flight
            flight = Flight("AirCanada", flight_external.price, request, self) 
            flights.append(flight)
        return flights


    def reserve(self, reservation: FlightReservation):
        flight = self._to_aircanada_flight_external(reservation.flight)
        customers_info = self._to_aircanada_customers_info_eternal(reservation.customers_info)
        # once we have both flight and customer info in external format
        # we contact the APIs to reserve the flight and give them the required info
        return AirCanadaOnlineAPI.reserve_flight(flight, customers_info)# which are in the format of aircanada

    def cancel(self, reservation):
        return AirCanadaOnlineAPI.cancel_flight(reservation.confirmation_id)

    @staticmethod
    def _to_aircanada_flight_external(flight: Flight):
        # this will take the flight and convert it to aircanada flight
        return AirCanadaFlight(flight.total_cost, flight.request.datetime_from, flight.request.datetime_to)

    @staticmethod
    def _to_aircanada_customers_info_eternal(customersinfo: list):
        # and the same here
        # convert list of customer iinfo to aircanada customer info
        customersinfo_external = []
        
        for customer in customersinfo:
            customer: CustomerInfo = customer
            #it means that customer is of type(instance) CustomerInfo
            customersinfo_external.append(AirCanadaCustomerInfo(customer.name, customer.passport_id, customer.birthdate))
        
        return customersinfo_external