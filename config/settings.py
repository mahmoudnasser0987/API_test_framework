"""
Configuration settings for the API test framework.
Centralizes base URLs, credentials, timeouts, and other settings.
"""

import os


class APIConfig:
    """API connection settings."""

    # RESTful-Booker API — a free, public REST API for testing
    # https://restful-booker.herokuapp.com/apidoc/index.html
    BASE_URL = os.getenv("API_BASE_URL", "https://restful-booker.herokuapp.com")

    # Default timeout for requests (seconds)
    REQUEST_TIMEOUT = 30

    # Auth credentials for the API (public test credentials)
    AUTH_USERNAME = os.getenv("API_USERNAME", "admin")
    AUTH_PASSWORD = os.getenv("API_PASSWORD", "password123")


class Headers:
    """Common HTTP headers."""

    JSON = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
