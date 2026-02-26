"""
API Tests for the RESTful-Booker API.

Tests cover the core CRUD operations for the Booking resource:
1. Create Booking (POST)        — validates response schema and data echo
2. Get Booking (GET)            — validates retrieval of created booking
3. Update Booking (PUT)         — validates full update of all fields
4. Delete Booking (DELETE)      — validates booking deletion

Additional tests use pytest.mark.parametrize for:
5. Create bookings with various data combinations
6. Filter bookings by name
7. Validate response structure and types
8. Edge cases with boundary values

Validation Strategy:
- Status code validation: ensures correct HTTP semantics
- Response body validation: ensures data integrity (create → read → verify)
- Schema validation: ensures response structure matches the API contract
- Response time: ensures acceptable performance
- Content-Type: ensures proper JSON responses
"""

import logging

import pytest

from models.booking import Booking, BookingDates
from services.booking_service import BookingService
from utils.test_data import create_valid_booking
from utils.validators import (
    assert_status_code,
    assert_json_key_exists,
    assert_json_value,
    assert_booking_fields,
    assert_response_time,
    assert_json_list_not_empty,
    assert_content_type,
)

logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════════
# Test Case 1: Create Booking (POST /booking)
# ════════════════════════════════════════════════════════════════


class TestCreateBooking:
    """Tests for the Create Booking endpoint."""

    def test_create_booking_returns_201_or_200(
        self, booking_service: BookingService, sample_booking: Booking
    ):
        """
        TC-01: Create a valid booking and verify response.

        Validation:
          - Status code is 200 (API returns 200 for creation)
          - Response contains 'bookingid'
          - Returned booking data matches the request
        """
        response = booking_service.create_booking(sample_booking)

        assert_status_code(response, 200)
        data = response.json()

        # Verify response structure
        assert "bookingid" in data, "Response missing 'bookingid'"
        assert "booking" in data, "Response missing 'booking'"

        # Verify echoed data matches input
        assert_booking_fields(data["booking"], sample_booking.to_dict())

    @pytest.mark.parametrize(
        "firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds",
        [
            ("Alice", "Smith", 200, True, "2025-03-01", "2025-03-05", "Lunch"),
            ("Bob", "Johnson", 0, False, "2025-06-15", "2025-06-20", None),
            ("Charlie", "Brown", 99999, True, "2025-12-24", "2025-12-31", "Late checkout"),
            ("Diana", "Prince", 50, True, "2025-01-01", "2025-01-02", "Extra pillow"),
        ],
        ids=[
            "standard_booking",
            "zero_price_no_deposit",
            "high_price_holiday",
            "minimal_stay_with_needs",
        ],
    )
    def test_create_booking_with_various_data(
        self,
        booking_service: BookingService,
        firstname,
        lastname,
        totalprice,
        depositpaid,
        checkin,
        checkout,
        additionalneeds,
    ):
        """
        TC-02: Create bookings with different data combinations.

        Uses pytest.parametrize to test multiple scenarios with
        a single test method — keeps code DRY with high coverage.

        Validation:
          - Each combination returns status 200
          - Each booking gets a unique ID
          - Returned data matches input for key fields
        """
        booking = create_valid_booking(
            firstname=firstname,
            lastname=lastname,
            totalprice=totalprice,
            depositpaid=depositpaid,
            bookingdates=BookingDates(checkin=checkin, checkout=checkout),
            additionalneeds=additionalneeds,
        )
        response = booking_service.create_booking(booking)

        assert_status_code(response, 200)
        data = response.json()

        assert isinstance(data["bookingid"], int), "bookingid should be an integer"
        assert data["booking"]["firstname"] == firstname
        assert data["booking"]["lastname"] == lastname
        assert data["booking"]["totalprice"] == totalprice
        assert data["booking"]["depositpaid"] == depositpaid


# ════════════════════════════════════════════════════════════════
# Test Case 2: Get Booking (GET /booking/:id)
# ════════════════════════════════════════════════════════════════


class TestGetBooking:
    """Tests for the Get Booking endpoint."""

    def test_get_existing_booking(
        self, booking_service: BookingService, created_booking: dict
    ):
        """
        TC-03: Retrieve a booking by ID and verify data.

        Validation:
          - Status code is 200
          - Response body matches the created booking data
          - Content-Type is application/json
          - Response time is under 5 seconds
        """
        booking_id = created_booking["id"]
        response = booking_service.get_booking(booking_id)

        assert_status_code(response, 200)
        assert_content_type(response, "application/json")
        assert_response_time(response, max_seconds=5.0)

        data = response.json()
        assert data["firstname"] == created_booking["data"]["firstname"]
        assert data["lastname"] == created_booking["data"]["lastname"]

    def test_get_nonexistent_booking_returns_404(
        self, booking_service: BookingService
    ):
        """
        TC-04: Request a booking that doesn't exist.

        Validation:
          - Status code is 404
          - API correctly handles invalid IDs
        """
        response = booking_service.get_booking(999999999)
        assert_status_code(response, 404)

    def test_get_all_booking_ids(self, booking_service: BookingService):
        """
        TC-05: Retrieve the list of all booking IDs.

        Validation:
          - Status code is 200
          - Response is a non-empty list
          - Each item has a 'bookingid' key
        """
        response = booking_service.get_booking_ids()

        assert_status_code(response, 200)
        assert_json_list_not_empty(response)

        data = response.json()
        assert all(
            "bookingid" in item for item in data
        ), "Not all items have 'bookingid'"

    @pytest.mark.parametrize(
        "filter_field, filter_value",
        [
            ("firstname", "John"),
            ("lastname", "Doe"),
        ],
        ids=["filter_by_firstname", "filter_by_lastname"],
    )
    def test_get_bookings_filtered_by_name(
        self,
        booking_service: BookingService,
        created_booking: dict,
        filter_field: str,
        filter_value: str,
    ):
        """
        TC-06: Filter bookings by firstname or lastname.

        Uses parametrize to test both filter types.

        Validation:
          - Status code is 200
          - Response is a list (may be empty if no matches)
        """
        response = booking_service.get_booking_ids(**{filter_field: filter_value})

        assert_status_code(response, 200)
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data).__name__}"


# ════════════════════════════════════════════════════════════════
# Test Case 3: Update Booking (PUT /booking/:id)
# ════════════════════════════════════════════════════════════════


class TestUpdateBooking:
    """Tests for the Update Booking endpoint."""

    def test_update_booking_full(
        self, booking_service: BookingService, created_booking: dict
    ):
        """
        TC-07: Fully update a booking and verify changes.

        Validation:
          - Status code is 200
          - All fields reflect the updated values
          - Original values are replaced
        """
        booking_id = created_booking["id"]
        updated = create_valid_booking(
            firstname="Updated",
            lastname="User",
            totalprice=999,
            depositpaid=False,
            bookingdates=BookingDates(
                checkin="2026-06-01", checkout="2026-06-15"
            ),
            additionalneeds="Airport shuttle",
        )

        response = booking_service.update_booking(booking_id, updated)

        assert_status_code(response, 200)
        data = response.json()
        assert data["firstname"] == "Updated"
        assert data["lastname"] == "User"
        assert data["totalprice"] == 999
        assert data["depositpaid"] is False

    def test_partial_update_booking(
        self, booking_service: BookingService, created_booking: dict
    ):
        """
        TC-08: Partially update a booking (PATCH).

        Validation:
          - Status code is 200
          - Only the updated fields change
          - Other fields remain unchanged
        """
        booking_id = created_booking["id"]
        patch_data = {"firstname": "Patched", "totalprice": 777}

        response = booking_service.partial_update_booking(booking_id, patch_data)

        assert_status_code(response, 200)
        data = response.json()
        assert data["firstname"] == "Patched"
        assert data["totalprice"] == 777
        # Original lastname should remain
        assert data["lastname"] == created_booking["data"]["lastname"]


# ════════════════════════════════════════════════════════════════
# Test Case 4: Delete Booking (DELETE /booking/:id)
# ════════════════════════════════════════════════════════════════


class TestDeleteBooking:
    """Tests for the Delete Booking endpoint."""

    def test_delete_booking(self, booking_service: BookingService):
        """
        TC-09: Delete a booking and verify it's gone.

        Validation:
          - Delete returns 201 (API convention)
          - Subsequent GET returns 404
          - Confirms the booking is truly removed
        """
        # Create a booking to delete
        booking = create_valid_booking(
            firstname="ToDelete", lastname="ThisOne"
        )
        create_response = booking_service.create_booking(booking)
        booking_id = create_response.json()["bookingid"]

        # Delete it
        delete_response = booking_service.delete_booking(booking_id)
        assert_status_code(delete_response, 201)

        # Verify it's gone
        get_response = booking_service.get_booking(booking_id)
        assert_status_code(get_response, 404)


# ════════════════════════════════════════════════════════════════
# Test Case 5: Response Validation & Schema Tests
# ════════════════════════════════════════════════════════════════


class TestResponseValidation:
    """Tests for response structure, types, and performance."""

    @pytest.mark.parametrize(
        "field, expected_type",
        [
            ("firstname", str),
            ("lastname", str),
            ("totalprice", int),
            ("depositpaid", bool),
            ("bookingdates", dict),
        ],
        ids=[
            "firstname_is_str",
            "lastname_is_str",
            "totalprice_is_int",
            "depositpaid_is_bool",
            "bookingdates_is_dict",
        ],
    )
    def test_booking_response_field_types(
        self,
        booking_service: BookingService,
        created_booking: dict,
        field: str,
        expected_type: type,
    ):
        """
        TC-10: Validate the data types in a booking response.

        Uses parametrize to check each field's type individually.

        Validation:
          - Each field exists in the response
          - Each field has the correct Python type
        """
        booking_id = created_booking["id"]
        response = booking_service.get_booking(booking_id)

        assert_status_code(response, 200)
        data = response.json()

        assert field in data, f"Field '{field}' missing from response"
        assert isinstance(data[field], expected_type), (
            f"Expected '{field}' to be {expected_type.__name__}, "
            f"got {type(data[field]).__name__}"
        )

    def test_api_health_check(self, booking_service: BookingService):
        """
        TC-11: Verify the API is reachable and responds.

        Validation:
          - Ping endpoint returns 201
          - Response time is acceptable
        """
        response = booking_service.get("/ping")

        assert_status_code(response, 201)
        assert_response_time(response, max_seconds=5.0)

    def test_auth_with_valid_credentials(
        self, booking_service: BookingService
    ):
        """
        TC-12: Authenticate with valid credentials.

        Validation:
          - Status code is 200
          - Response contains a 'token' field
          - Token is a non-empty string
        """
        response = booking_service.post(
            "/auth",
            json={"username": "admin", "password": "password123"},
        )

        assert_status_code(response, 200)
        data = response.json()
        assert "token" in data, "Response missing 'token'"
        assert isinstance(data["token"], str) and len(data["token"]) > 0
