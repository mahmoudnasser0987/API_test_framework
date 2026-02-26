"""
Test Case: <short description of what this test validates>
    1. Describe step 1 here
    2. Describe step 2 here
    ...

How to use this template:
    1. Copy this file into regression_suite/ and rename it:
       regression_suite/test_<feature>.py
    2. Rename the class: TestTemplate → Test<YourFeature>
    3. Rename the method: test_template → test_<your_scenario>
    4. Replace the step blocks with your real API calls and assertions
    5. Delete this header comment block

Available fixtures (add as method arguments — no setup required):
    booking_service  — pre-configured BookingService client (session-scoped)
    auth_token       — authentication token string
    sample_booking   — a valid Booking model instance
    created_booking  — a booking already created in the API (returns dict with 'id' and 'data')

Available validators (import from utils.validators):
    assert_status_code(response, expected_code)
    assert_json_key_exists(response, key)
    assert_json_value(response, key, expected_value)
    assert_booking_fields(booking_data, expected_dict)
    assert_response_time(response, max_seconds)
    assert_json_list_not_empty(response)
    assert_content_type(response, expected_type)

Available test data helpers (import from utils.test_data):
    create_valid_booking(**overrides)   — returns a Booking with sensible defaults
    create_booking_payload(**overrides) — returns a raw dict payload
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
    assert_content_type,
)

logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════════
# Rename: TestTemplate → Test<YourFeature>
# ════════════════════════════════════════════════════════════════


class TestTemplate:
    """
    Test suite for: <describe what this test class covers>

    Rename this class to match the feature being tested.
    """

    # ── Test inputs ────────────────────────────────────────────
    # Define ALL data that drives this test here as class constants.
    # Examples:
    # FIRSTNAME = "Alice"
    # EXPECTED_STATUS = 200

    # ──────────────────────────────────────────────────────────────
    # @pytest.mark.smoke          ← uncomment to tag as a smoke test
    # @pytest.mark.regression     ← uncomment to tag as a regression test
    # ──────────────────────────────────────────────────────────────
    def test_template(self, booking_service: BookingService, sample_booking: Booking):
        """
        TC-XX: <describe what this test validates>

        Steps:
            1. ...
            2. ...

        Validation:
            - ...
        """
        # ── Step 1: Create / call the API ──────────────────────
        logger.info("Step 1: <describe>")
        response = booking_service.create_booking(sample_booking)

        # ── Step 2: Validate response ──────────────────────────
        logger.info("Step 2: Validating response")
        assert_status_code(response, 200)

        data = response.json()
        assert "bookingid" in data, "Response missing 'bookingid'"

        # ── Step 3: Additional assertions ──────────────────────
        logger.info("Step 3: Verifying data")
        assert_booking_fields(data["booking"], sample_booking.to_dict())

        logger.info("Test passed ✓")
