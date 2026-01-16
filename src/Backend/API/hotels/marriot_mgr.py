from ..common.reservation import IReservation
from ..common.customer_info import CustomerInfo
from .hotel_common import HotelRequest, Hotel, HotelReservation
from .marriott_external import MarriottCustomerInfo, MarriottRoom, MarriottHotelAPI

class MarriotHotelManager(IReservation):
    def __init__(self):
        pass

    @staticmethod
    def _to_marriot_room_external(hotel: Hotel):
        return MarriottRoom(hotel.request.room_type, hotel.request.num_rooms, hotel.price_per_night,
                            hotel.request.date_from, hotel.request.date_to)
    
    @staticmethod
    def to_marriot_customers_info_external(customersinfo: list):
        customersinfo_external = []

        for customer in customersinfo:
            customer: CustomerInfo = customer

            customersinfo_external.append(MarriottCustomerInfo(customer.name, customer.passport_id, customer.birthdate))
        
        return customersinfo_external
    
    def search(self, request: HotelRequest):
        hotels_external = MarriottHotelAPI.search_available_rooms(request.location, request.date_from,
                                                                  request.date_to, request.adults,
                                                                  request.children, request.num_rooms)

        hotels = []
        
        for hotel_external in hotels_external:
            hotel = Hotel("Marriot", hotel_external.price_per_night, request, self)
            hotels.append(hotel)

        return hotels
    
    def reserve(self, reservation: HotelReservation):
        hotel = self._to_marriot_room_external(reservation.hotel)
        customers_info = self.to_marriot_customers_info_external(reservation.customers_info)
        return MarriottHotelAPI.do_room_reservation(hotel, customers_info)
    
    def cancel(self, reservation: HotelReservation):
        return MarriottHotelAPI.cancel_room(reservation.confirmation_id)
    
    