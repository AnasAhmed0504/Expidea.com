# Expedia.com - Flight & Hotel Booking System

A Python-based flight and hotel booking management system with user authentication, itinerary management, and payment processing capabilities.

## Functional Requirements
In expedia, a user creates several itineraries, each itinerary consists of
several reservations as following

0 or more flights, hotels, cars, etc. E.g. 4 flights, 2 hotels and 2 cars.

### Each reservation may has its own info
  
  E.g. Hotel cost: total nights x price per night
  
  The itinerary cost = sum of its inner reservations
  
### For simplicity

2 types of users: Admin & customer. Focus of your code is on Customer part

Don’t burn time validating inputs or minor concerns

The core goal is OOP design skills

## APIs
Expedia needs to contact several APIs

● Flights APIs

  ○ Companies such as AirCanada, TurkishAirlines and others allow them to do online query to
get current available flights

  ○ Then after the customer make a choice, you ask them to cancel/reserve
  
● Hotel APIs: In a similar way, hotels such as Hilton, Marriott provide APIs

● Payments: Expedia uses one of the payments APIs (e.g. Square/Stripe, etc)

● Follow the homework. Your code should be **loosely coupled** with these APIs

● Your code should be extensible: Future similar APIs might be used

● Content of the APIs is not hours. Put dummy data to simulate

● APIs code is given. Download it.

## Notes (API Abstraction Architecture)

### The Challenge

Direct dependency on specific external APIs creates tight coupling and makes the system inflexible and difficult to maintain. To solve this, we implement an abstraction layer between our application and external providers.

### The Solution

Each external API provider has a corresponding Manager class that acts as an intermediary. This means the application never directly contacts external APIs—instead, it communicates through standardized managers.

For example, Air Canada's external API is kept separate from our application logic through the `AirCanadaManager` class. This manager is responsible for all interactions with Air Canada's services.

### How Each Manager Works

Every manager inherits from the `IReservationManager` interface, ensuring they all follow the same contract with three core operations: search, reserve, and cancel. This standardization means any provider can be swapped out without affecting the rest of the system.

### The Request Flow

When searching for flights, the process follows this sequence:

1. **Receive Internal Request** - The customer initiates a search with standard internal parameters
2. **Extract Required Information** - The manager extracts the relevant data from the request
3. **Contact External API** - The manager reaches out to the provider's API with the extracted information
4. **Convert to Internal Format** - The provider returns data in their own format, which the manager converts to our standardized internal format
5. **Return Results** - The application receives consistent, format-agnostic flight information

### The Reservation Process

Reservations follow a similar pattern of format conversion:

1. **Prepare Data** - Flight and customer information are collected in our internal format
2. **Convert to External Format** - The manager transforms the data into the provider's expected format
3. **Contact External API** - The reservation request is sent to the provider
4. **Receive Confirmation** - The provider returns a confirmation ID
5. **Return to Application** - The confirmation is passed back to the application

### Why This Matters

This architecture provides several key benefits:

- **Provider Independence** - The application is not locked into any specific external API
- **Easy Integration** - New providers can be added by simply creating a new manager class
- **Consistency** - All providers expose the same interface to the application
- **Maintainability** - Changes in external APIs only require updates to their corresponding manager
- **Scalability** - The system can grow to support dozens of providers without architectural changes## Features

- **User Management**
  - User registration and login
  - Customer profile viewing
  - Support for multiple user types (Customer, Admin)

- **Flight Management**
  - Search flights from multiple airlines (Air Canada, Turkish Airlines)
  - Browse available flights
  - Add flights to itinerary
  - Flight reservation and cancellation

- **Hotel Management**
  - Search hotels from multiple providers (Marriot, Hilton)
  - Browse available rooms
  - Add hotels to itinerary
  - Hotel reservation and cancellation

- **Itinerary Management**
  - Create custom itineraries
  - Combine multiple flights and hotels
  - View itinerary details and total cost
  - List all saved itineraries

- **Payment Processing**
  - Multiple payment methods (PayPal, Stripe)
  - Secure payment card management
  - Transaction handling and cancellation
  - Payment error handling

## Architecture

### Design Patterns Used

- **Abstract Base Classes (ABC)** - Define common interfaces for managers and reservations
- **Manager Pattern** - Separate managers for flights, hotels, and payments
- **Factory Pattern** - Create reservation objects based on type
- **Aggregator Pattern** - Multiple airline/hotel providers aggregated into single search


## Technologies Used

- **Language:** Python 3.10+
- **Architecture:** Object-Oriented Programming (OOP)
- **Design Patterns:** Abstract Base Classes, Manager Pattern, Aggregator Pattern
- **External Integrations:** Flight/Hotel APIs, Payment Gateways

## Key Classes

### User Management
- `User` - Base user class
- `Customer` - Customer user with payment cards
- `Admin` - Administrator user (future extension)
- `UsersManager` - Manages user operations

### Reservations
- `IReservation` - Abstract reservation interface
- `FlightReservation` - Individual flight booking
- `HotelReservation` - Individual hotel booking
- `ItineraryReservation` - Collection of reservations

### Managers
- `FlightManager` - Aggregates flight managers
- `HotelManager` - Aggregates hotel managers
- `CustomerBackendManager` - Handles all customer operations

## Error Handling

The system includes custom exceptions for:
- `ExpediaPaymentException` - Payment processing failures
- `ExpediaReservationException` - Reservation failures

## Author

Anas Yousry

## Acknowledgments

- Design inspired by real-world booking systems 
- Built as part of Software Engineering coursework

## Contact

For questions or feedback, please contact:
- GitHub: [@AnasYousry2603](https://github.com/AnasYousry2603)
- Email: AnasYousry2603@gmail.com

---

**Last Updated:** January 16, 2026

