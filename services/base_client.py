"""
Base API Client - Foundation for all service classes.

Provides a reusable HTTP client with:
- Session management for connection pooling
- Common headers
- Logging of requests/responses
- Timeout handling
- Response validation helpers

All service classes inherit from this base client.
"""

import logging
from typing import Optional

import requests

from config.settings import APIConfig, Headers

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """
    Base HTTP client for API interactions.

    Wraps the `requests` library with logging, timeouts, and
    session reuse for clean, maintainable API tests.
    """

    def __init__(self, base_url: str = None):
        self.base_url = base_url or APIConfig.BASE_URL
        self.session = requests.Session()
        self.session.headers.update(Headers.JSON)
        self.timeout = APIConfig.REQUEST_TIMEOUT

    def _url(self, endpoint: str) -> str:
        """Build the full URL for an endpoint."""
        return f"{self.base_url}{endpoint}"

    def _log_request(self, method: str, url: str, **kwargs):
        """Log outgoing request details."""
        logger.info(f"REQUEST  → {method} {url}")
        if "json" in kwargs:
            logger.debug(f"  Body: {kwargs['json']}")
        if "params" in kwargs:
            logger.debug(f"  Params: {kwargs['params']}")

    def _log_response(self, response: requests.Response):
        """Log incoming response details."""
        logger.info(
            f"RESPONSE ← {response.status_code} "
            f"({response.elapsed.total_seconds():.2f}s)"
        )
        logger.debug(f"  Body: {response.text[:500]}")

    # ── HTTP Methods ────────────────────────────────────────────

    def get(
        self,
        endpoint: str,
        params: dict = None,
        headers: dict = None,
    ) -> requests.Response:
        """Send a GET request."""
        url = self._url(endpoint)
        self._log_request("GET", url, params=params)
        response = self.session.get(
            url, params=params, headers=headers, timeout=self.timeout
        )
        self._log_response(response)
        return response

    def post(
        self,
        endpoint: str,
        json: dict = None,
        headers: dict = None,
    ) -> requests.Response:
        """Send a POST request."""
        url = self._url(endpoint)
        self._log_request("POST", url, json=json)
        response = self.session.post(
            url, json=json, headers=headers, timeout=self.timeout
        )
        self._log_response(response)
        return response

    def put(
        self,
        endpoint: str,
        json: dict = None,
        headers: dict = None,
    ) -> requests.Response:
        """Send a PUT request."""
        url = self._url(endpoint)
        self._log_request("PUT", url, json=json)
        response = self.session.put(
            url, json=json, headers=headers, timeout=self.timeout
        )
        self._log_response(response)
        return response

    def patch(
        self,
        endpoint: str,
        json: dict = None,
        headers: dict = None,
    ) -> requests.Response:
        """Send a PATCH request."""
        url = self._url(endpoint)
        self._log_request("PATCH", url, json=json)
        response = self.session.patch(
            url, json=json, headers=headers, timeout=self.timeout
        )
        self._log_response(response)
        return response

    def delete(
        self,
        endpoint: str,
        headers: dict = None,
    ) -> requests.Response:
        """Send a DELETE request."""
        url = self._url(endpoint)
        self._log_request("DELETE", url)
        response = self.session.delete(
            url, headers=headers, timeout=self.timeout
        )
        self._log_response(response)
        return response

    def close(self):
        """Close the session."""
        self.session.close()
