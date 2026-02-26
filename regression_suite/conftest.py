"""
Pytest fixtures for the API test framework.

Provides shared setup/teardown logic:
- BookingService instance management
- Pre-created booking for tests that need existing data
- Logging configuration
"""

import logging

import pytest

from models.booking import Booking, BookingDates
from services.booking_service import BookingService
from utils.test_data import create_valid_booking

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def booking_service() -> BookingService:
    """
    Provide a BookingService instance for the test session.

    Session-scoped to reuse the HTTP session and auth token
    across all tests, improving performance.
    """
    service = BookingService()
    yield service
    service.close()


@pytest.fixture(scope="session")
def auth_token(booking_service: BookingService) -> str:
    """Get an authentication token for the session."""
    return booking_service.authenticate()


@pytest.fixture
def sample_booking() -> Booking:
    """Provide a sample valid booking for testing."""
    return create_valid_booking()


@pytest.fixture
def created_booking(booking_service: BookingService, sample_booking: Booking):
    """
    Create a booking and return its ID and data.

    Useful for tests that need an existing booking (GET, PUT, DELETE).
    """
    response = booking_service.create_booking(sample_booking)
    data = response.json()
    booking_id = data["bookingid"]
    logger.info(f"Created test booking with ID: {booking_id}")

    yield {"id": booking_id, "data": data["booking"]}

    # Cleanup: attempt to delete the booking after test
    try:
        booking_service.delete_booking(booking_id)
        logger.info(f"Cleaned up booking ID: {booking_id}")
    except Exception:
        logger.warning(f"Could not clean up booking ID: {booking_id}")
