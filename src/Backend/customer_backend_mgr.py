from .API.flights.flight_mgr import FlightManager
from .API.flights.flight_common import FlightRequest
from .API.hotels.hotel_common import HotelRequest
from .API.hotels.hotels_mgr import HotelManager
from .exceptions.exceptions import ExpediaPaymentException, ExpediaReservationException
from .API.payment.paypal_payment import PayPalPayment
from .API.common.reservation import ItineraryReservation, IReservation


class CustomerBackendManager:
    def __init__(self, customer):
        self.customer = customer
        self.hotels_manager = HotelManager()
        self.flights_manager = FlightManager()
        #remember that they are several hotel/flights managers
        self.payment_api = PayPalPayment() #--> only one payment at a time

    
    def search_flights(self, request: FlightRequest):
        return self.flights_manager.search(request)

    def search_hotels(self, request: HotelRequest):
        return self.hotels_manager.search(request)

    def get_payment_choices(self):
        return [repr(card) for card in self.customer.payment_cards]

    def _make_payment(self, cost, card):
        self.payment_api.set_user_info(card.owner_name, card.address)
        self.payment_api.set_card_info(card.card_number, card.expiry_date, card.security_code)
        status, transaction_id = self.payment_api.make_payment(cost)
        
        return status, transaction_id
    

    def _cancel_payment(self, transaction_id):
        self.payment_api.cancel_payment(transaction_id)

    def _cancel_reservations(self, reservations):
        #assume cancellation will always work, in reality no
        for reservation in reservations:
            reservation.mgr.cancel(reservation)

    def _reserve(self, reservations):
        """Reserve all the given reservations, if some of them fails, then cancel all
        return true if succeeded
        """
        if not isinstance(reservations, list):
            reservations = [reservations] #let's make it always a list
        
        reserved_items = [] #track the reserved
        for reservation in reservations:
            confirmation_id = reservation.mgr.reserve(reservation)

            if confirmation_id:
                reservation.confirmation_id = confirmation_id
                reserved_items.append(confirmation_id)
            
            else:
                reservation.mgr.cancel(reservation)#cancel all reserved so far
                return False
        return True
        

    def pay_and_reserve(self, reservation: IReservation, payment_card_idx):
        payment_card = self.customer.payment_cards[payment_card_idx]
        total_cost = reservation.total_cost
        is_paid, transaction_id = self._make_payment(total_cost, payment_card)

        if is_paid:
            if isinstance(reservation, IReservation):
                is_reserved = self._reserve(reservation.reservations)
            else:
                is_reserved = self._reserve(reservation)
        
            if not is_reserved:
                self._cancel_payment(transaction_id)
                raise ExpediaReservationException

        else:
            raise ExpediaPaymentException