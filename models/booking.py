"""
Data models for the Booking API.

Uses dataclasses for clean, type-safe representation of request
and response payloads. Models are framework building blocks that
make tests readable and data reusable.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class BookingDates:
    """Check-in and check-out dates for a booking."""

    checkin: str
    checkout: str


@dataclass
class Booking:
    """Representation of a booking payload."""

    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to a dictionary suitable for API requests."""
        data = {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "totalprice": self.totalprice,
            "depositpaid": self.depositpaid,
            "bookingdates": {
                "checkin": self.bookingdates.checkin,
                "checkout": self.bookingdates.checkout,
            },
        }
        if self.additionalneeds is not None:
            data["additionalneeds"] = self.additionalneeds
        return data


@dataclass
class BookingResponse:
    """Representation of the API response when creating a booking."""

    bookingid: int
    booking: dict
