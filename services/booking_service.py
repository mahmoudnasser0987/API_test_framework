"""
Booking Service - API client for the Booking endpoints.

Encapsulates all booking-related API calls. Tests interact with
this service layer instead of making raw HTTP calls, providing:
- Clean abstraction over endpoints
- Reusable across multiple test files
- Single point of change if the API contract changes
"""

import logging
from typing import Optional

import requests

from config.settings import APIConfig
from models.booking import Booking
from services.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class BookingService(BaseAPIClient):
    """Service class for the /booking endpoints."""

    ENDPOINT = "/booking"
    AUTH_ENDPOINT = "/auth"

    def __init__(self):
        super().__init__()
        self._token: Optional[str] = None

    # ── Authentication ──────────────────────────────────────────

    def authenticate(
        self,
        username: str = None,
        password: str = None,
    ) -> str:
        """
        Get an authentication token.

        Args:
            username: API username (defaults to config value).
            password: API password (defaults to config value).

        Returns:
            Authentication token string.
        """
        payload = {
            "username": username or APIConfig.AUTH_USERNAME,
            "password": password or APIConfig.AUTH_PASSWORD,
        }
        response = self.post(self.AUTH_ENDPOINT, json=payload)
        self._token = response.json().get("token")
        logger.info("Authentication successful")
        return self._token

    @property
    def auth_headers(self) -> dict:
        """Get headers with authentication cookie."""
        if not self._token:
            self.authenticate()
        return {"Cookie": f"token={self._token}"}

    # ── CRUD Operations ─────────────────────────────────────────

    def get_booking_ids(
        self,
        firstname: str = None,
        lastname: str = None,
        checkin: str = None,
        checkout: str = None,
    ) -> requests.Response:
        """
        Get all booking IDs, optionally filtered.

        Args:
            firstname: Filter by guest first name.
            lastname: Filter by guest last name.
            checkin: Filter by check-in date (YYYY-MM-DD).
            checkout: Filter by check-out date (YYYY-MM-DD).
        """
        params = {}
        if firstname:
            params["firstname"] = firstname
        if lastname:
            params["lastname"] = lastname
        if checkin:
            params["checkin"] = checkin
        if checkout:
            params["checkout"] = checkout

        return self.get(self.ENDPOINT, params=params)

    def get_booking(self, booking_id: int) -> requests.Response:
        """Get a specific booking by ID."""
        return self.get(f"{self.ENDPOINT}/{booking_id}")

    def create_booking(self, booking: Booking) -> requests.Response:
        """
        Create a new booking.

        Args:
            booking: Booking data model instance.
        """
        return self.post(self.ENDPOINT, json=booking.to_dict())

    def update_booking(
        self, booking_id: int, booking: Booking
    ) -> requests.Response:
        """
        Update an existing booking (full update).

        Args:
            booking_id: ID of the booking to update.
            booking: Complete booking data.
        """
        return self.put(
            f"{self.ENDPOINT}/{booking_id}",
            json=booking.to_dict(),
            headers=self.auth_headers,
        )

    def partial_update_booking(
        self, booking_id: int, data: dict
    ) -> requests.Response:
        """
        Partially update a booking.

        Args:
            booking_id: ID of the booking to update.
            data: Dictionary of fields to update.
        """
        return self.patch(
            f"{self.ENDPOINT}/{booking_id}",
            json=data,
            headers=self.auth_headers,
        )

    def delete_booking(self, booking_id: int) -> requests.Response:
        """
        Delete a booking.

        Args:
            booking_id: ID of the booking to delete.
        """
        return self.delete(
            f"{self.ENDPOINT}/{booking_id}",
            headers=self.auth_headers,
        )
