"""
Test data helpers - Factories for generating test data.

Provides reusable functions to create valid and invalid test payloads,
keeping test files clean and focused on assertions.
"""

from models.booking import Booking, BookingDates


def create_valid_booking(**overrides) -> Booking:
    """
    Create a valid Booking with sensible defaults.

    Any field can be overridden via keyword arguments.

    Returns:
        A Booking instance with valid test data.
    """
    defaults = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": BookingDates(
            checkin="2025-01-01",
            checkout="2025-01-10",
        ),
        "additionalneeds": "Breakfast",
    }
    defaults.update(overrides)

    # Handle bookingdates if passed as a dict
    if isinstance(defaults["bookingdates"], dict):
        defaults["bookingdates"] = BookingDates(**defaults["bookingdates"])

    return Booking(**defaults)


def create_booking_payload(**overrides) -> dict:
    """Create a valid booking payload as a dictionary."""
    return create_valid_booking(**overrides).to_dict()
