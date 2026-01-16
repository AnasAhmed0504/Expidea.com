from .turkish_external import TurkishOnlineAPI, TurkishFlight, TurkishCustomerInfo
from .flight_common import Flight, FlightRequest, FlightReservation
from ..common.reservation import IReservationManager
from ..common.customer_info import CustomerInfo


class TurkishAirlinesManager(IReservationManager):
    def __init__(self):
        self.api = TurkishOnlineAPI()

    def search(self, request):
        self.api.set_from_to_info(request.datetime_from, request.from_loc, request.datetime_to, request.to_loc)
        self.api.set_passengers_info(request.infants, request.children, request.adults)

        flights_external = self.api.get_available_flights()
        # Convert from external API format to internal format
        flights = []
        for flight_external in flights_external:
            #pass self as the generating manager
            flight = Flight("TurkishAirlines", flight_external.cost, request, self)
            flights.append(flight)
        return flights
    
    @staticmethod
    def _to_turkish_flight_external(flight: Flight):
        return TurkishFlight(flight.total_cost, flight.request.datetime_from, flight.request.datetime_to)

    @staticmethod
    def _to_turkish_customers_info_external(customersinfo: list):
        customersinfo_external = []

        for customer in customersinfo:
            customer: CustomerInfo = customer
            #it means that customer is of type(instance) CustomerInfo
            customersinfo_external.append(TurkishCustomerInfo(customer.name, customer.passport_id, customer.birthdate))
    
    
    def reserve(self, reservation: FlightReservation):
        flight = self._to_turkish_flight_external(reservation.flight)
        customers = self._to_turkish_customers_info_external(reservation.customers_info)
        return TurkishOnlineAPI.reserve_flight(customers, flight)

    def cancel(self, reservation):
        return TurkishOnlineAPI.cancel_flight(reservation.confirmation_id)

    