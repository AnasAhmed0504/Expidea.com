from .utils import get_menu_choice
from..Backend.API.flights.flight_common import FlightRequest, FlightReservation
from ..Backend.API.hotels.hotel_common import HotelRequest, HotelReservation
from ..Backend.API.common.customer_info import CustomerInfo
from ..Backend.user import Customer
from ..Backend.API.common.reservation import ItineraryReservation
from ..Backend.customer_backend_mgr import CustomerBackendManager
from ..Backend.exceptions.exceptions import ExpediaPaymentException, ExpediaReservationException

class CustomerFrontendManager:
    def __init__(self, customer: Customer):
        self.customer = customer
        self.customer_backend_mgr = CustomerBackendManager(customer)
        self.current_itinerary = ItineraryReservation()
        self.itineraries = []

    def _load_data(self):
        s = '1'
        request = FlightRequest(s, s, s, s, s, s, s)
        flights = self.customer_backend_mgr.search_flights(request)
        customer = CustomerInfo(self.customer.name, None, None)  # temp. in practice build
        reservation = FlightReservation(flights[0], [customer])
        status = self.customer_backend_mgr._reserve(reservation)
        self.current_itinerary.reservations.append(reservation)

        s = '2'
        request = FlightRequest(s, s, s, s, s, s, s)
        flights = self.customer_backend_mgr.search_flights(request)
        customer = CustomerInfo(self.customer.name, None, None)  # temp. in practice build
        reservation = FlightReservation(flights[1], [customer])
        self.current_itinerary.reservations.append(reservation)
        self.reserve_itinerary()

        s = '2'
        request = FlightRequest(s, s, s, s, s, s, s)
        flights = self.customer_backend_mgr.search_flights(request)
        customer = CustomerInfo(self.customer.name, None, None)  # temp. in practice build
        reservation = FlightReservation(flights[2], [customer])
        status = self.customer_backend_mgr._reserve(reservation)
        self.current_itinerary.reservations.append(reservation)

        s = '4'
        request = FlightRequest(s, s, s, s, s, s, s)
        flights = self.customer_backend_mgr.search_flights(request)
        customer = CustomerInfo(self.customer.name, None, None)  # temp. in practice build
        reservation = FlightReservation(flights[3], [customer])
        self.current_itinerary.reservations.append(reservation)

        s = '5'
        request = HotelRequest(s, s, s, s, s, s, s)
        hotels = self.customer_backend_mgr.search_hotels(request)
        customer = CustomerInfo(self.customer.name, None, None)  # temp. in practice build
        reservation = HotelReservation(hotels[0], [customer])
        self.current_itinerary.reservations.append(reservation)

        self.reserve_itinerary()

        self.list_itineraries()


    def print_menu(self):
        msgs = ['View profile', 'Make itinerary', 'List my itineraries', 'Logout']
        return get_menu_choice(f"Hello {self.customer}:", msgs)


    def run(self):
        funcs = [self.view_profile, self.make_itinerary, self.list_itineraries]

        while True:
            choice = self.print_menu()
            if choice == 4:
                self.customer = None
                return
            else:
                funcs[choice - 1]()


    def view_profile(self):   
        print("=== Customer Profile ===")
        print(f"Name: {self.customer.name}")
        print(f"Username: {self.customer.user_name}")
        print(f"Email: {self.customer.email}")
        if hasattr(self.customer, 'payment_cards'):
            print(f"Payment Cards on File: {len(self.customer.payment_cards)}")
        print()

    def make_itinerary(self):
        self.current_itinerary = ItineraryReservation()
        funcs = [self.add_flight, self.add_hotel, self.reserve_itinerary, self.cancel_itinerary]
        
        def print_menu():
            msgs = ['Add Flight', 'Add Hotel', 'Reserve itinerary', 'Cancel itinerary']
            return get_menu_choice(f'Create your itinerary:', msgs)
        
        while True:
            choice = print_menu()
            funcs[choice - 1]()

            if choice >= 3:
                return


    def list_itineraries(self):
        if not self.itineraries:
            print("No iteneraries")
            return
        
        print(f'Listing {len(self.itineraries)} itineraries')
        for itin in self.itineraries:
            print(repr(itin), '\n')

    def add_flight(self):
        def read_flight_request():
            from_loc = input('Enter from: ')
            from_dte = input('Enter From Date (dd-mm-yy): ')
            to_loc = input('Enter To: ')
            to_dte = input('Enter Return Date (dd-mm-yy): ')
            # In practice we need to make sure valid int are given
            infants = int(input('Enter # of infants: '))
            children = int(input('Enter # of children: '))
            adults = int(input('Enter # of adults: '))

            return FlightRequest(from_dte, from_loc, to_dte, to_loc, infants, children, adults)
        
        request = read_flight_request()
        flights = self.customer_backend_mgr.search_flights(request)

        choice = get_menu_choice(f'Select a flight:', flights)

        customer = CustomerInfo(self.customer.name, None, None)    # temp. in practice build
        reservation = FlightReservation(flights[choice-1], [customer])
        self.current_itinerary.reservations.append(reservation)

    def add_hotel(self):
        def read_hotel_request():
            from_loc = input('Enter from: ')
            from_dte = input('Enter From Date (dd-mm-yy): ')
            to_loc = input('Enter To: ')
            to_dte = input('Enter Return Date (dd-mm-yy): ')
            # In practice we need to make sure valid int are given
            infants = int(input('Enter # of infants: '))
            children = int(input('Enter # of children: '))
            adults = int(input('Enter # of adults: '))

            return HotelRequest(from_dte, from_loc, to_dte, to_loc, infants, children, adults)

        request = read_hotel_request()
        hotels = self.customer_backend_mgr.search_hotels(request)

        choice = get_menu_choice(f'Select a flight:', hotels)

        customer = CustomerInfo(self.customer.name, None, None)    # temp. in practice build
        reservation = HotelReservation(hotels[choice-1], [customer])
        self.current_itinerary.reservations.append(reservation)


    def reserve_itinerary(self):
        if self.current_itinerary.reservations:
            choices = self.customer_backend_mgr.get_payment_choices()
            choice = get_menu_choice(f"Which kind of payment", choices)

            try:
                self.customer_backend_mgr.pay_and_reserve(self.current_itinerary, choice-1)
            except ExpediaPaymentException as e:
                print(e)
                print('Failed to pay. Review your balance')
            except ExpediaReservationException as e:
                print(e)
                print('Failed to complete reservation. Money will be returned shortly. Try again later')
            else:
                self.itineraries.append(self.current_itinerary)
                self.current_itinerary = ItineraryReservation()
                print('Successfully paid and reserved the trip')

        else:
            print('Nothing is added to reserve')

    def cancel_itinerary(self):
        self.current_itinerary = ItineraryReservation()