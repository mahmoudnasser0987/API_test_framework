"""
Response validators - Reusable assertion helpers for API tests.

Centralizes common validation patterns so tests are concise
and validation logic is consistent across the suite.
"""

import logging

import requests

logger = logging.getLogger(__name__)


def assert_status_code(response: requests.Response, expected: int):
    """Assert the response has the expected status code."""
    assert response.status_code == expected, (
        f"Expected status {expected}, got {response.status_code}. "
        f"Response: {response.text[:300]}"
    )


def assert_json_key_exists(response: requests.Response, key: str):
    """Assert a key exists in the JSON response."""
    data = response.json()
    assert key in data, f"Key '{key}' not found in response: {data}"


def assert_json_value(response: requests.Response, key: str, expected_value):
    """Assert a specific key has the expected value in the JSON response."""
    data = response.json()
    assert key in data, f"Key '{key}' not found in response: {data}"
    assert data[key] == expected_value, (
        f"Expected '{key}' = {expected_value}, got {data[key]}"
    )


def assert_booking_fields(booking_data: dict, expected: dict):
    """
    Assert that booking data contains the expected field values.

    Args:
        booking_data: The booking dictionary from the API response.
        expected: Dictionary of expected field values.
    """
    for key, value in expected.items():
        if key == "bookingdates":
            for date_key, date_val in value.items():
                assert booking_data["bookingdates"][date_key] == date_val, (
                    f"Expected bookingdates.{date_key} = '{date_val}', "
                    f"got '{booking_data['bookingdates'][date_key]}'"
                )
        else:
            assert booking_data[key] == value, (
                f"Expected '{key}' = '{value}', got '{booking_data[key]}'"
            )


def assert_response_time(response: requests.Response, max_seconds: float = 5.0):
    """Assert the response was received within an acceptable time."""
    elapsed = response.elapsed.total_seconds()
    assert elapsed < max_seconds, (
        f"Response took {elapsed:.2f}s, exceeding {max_seconds}s threshold"
    )


def assert_json_list_not_empty(response: requests.Response):
    """Assert the JSON response is a non-empty list."""
    data = response.json()
    assert isinstance(data, list), f"Expected a list, got {type(data).__name__}"
    assert len(data) > 0, "Expected non-empty list, got empty"


def assert_content_type(response: requests.Response, expected: str = "application/json"):
    """Assert the response Content-Type header."""
    content_type = response.headers.get("Content-Type", "")
    assert expected in content_type, (
        f"Expected Content-Type '{expected}', got '{content_type}'"
    )
