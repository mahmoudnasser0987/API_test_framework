# RESTful-Booker API Test Framework

A scalable, maintainable API test automation framework using **pytest** and a **service-layer architecture** for testing the [RESTful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) public API.

## Demo

<!-- Replace with your recorded GIF -->
![Test Run Demo](demo.gif)

## Test Cases

| TC ID  | Test Case                                  | Method | Endpoint            | Validation                                                         |
|--------|--------------------------------------------|--------|---------------------|--------------------------------------------------------------------|
| TC-01  | Create a valid booking                     | POST   | `/booking`          | Status 200, response contains bookingid, data echoed correctly     |
| TC-02  | Create bookings with various data (x4)     | POST   | `/booking`          | Status 200, unique ID, field values match (parametrized)           |
| TC-03  | Get existing booking by ID                 | GET    | `/booking/:id`      | Status 200, data matches, Content-Type JSON, response < 5s        |
| TC-04  | Get non-existent booking                   | GET    | `/booking/999999999`| Status 404                                                        |
| TC-05  | Get all booking IDs                        | GET    | `/booking`          | Status 200, non-empty list, each item has 'bookingid'             |
| TC-06  | Filter bookings by name (x2)              | GET    | `/booking?name=...` | Status 200, returns list (parametrized by firstname/lastname)      |
| TC-07  | Full update a booking                      | PUT    | `/booking/:id`      | Status 200, all fields updated correctly                           |
| TC-08  | Partial update a booking                   | PATCH  | `/booking/:id`      | Status 200, only changed fields updated, others unchanged          |
| TC-09  | Delete a booking                           | DELETE | `/booking/:id`      | Status 201, subsequent GET returns 404                             |
| TC-10  | Validate response field types (x5)         | GET    | `/booking/:id`      | Each field has correct type: str, int, bool, dict (parametrized)   |
| TC-11  | API health check                           | GET    | `/ping`             | Status 201, response < 5s                                         |
| TC-12  | Authentication with valid credentials      | POST   | `/auth`             | Status 200, response contains non-empty token                      |

> **Total:** 12 unique test cases (with parametrized expansion = **20+ test executions**)

## Validation Strategy

| Validation Type        | Purpose                                                      | Used In        |
|------------------------|--------------------------------------------------------------|----------------|
| **Status Code**        | Verifies correct HTTP semantics (200, 201, 404)              | All tests      |
| **Response Body**      | Ensures data integrity — created data matches when retrieved | TC-01 to TC-08 |
| **Schema/Type Check**  | Validates response structure and field types match API contract | TC-10        |
| **Response Time**      | Ensures API responds within acceptable performance bounds     | TC-03, TC-11   |
| **Content-Type**       | Verifies proper JSON content headers                          | TC-03          |
| **State Verification** | Confirms side effects (e.g., DELETE → GET returns 404)       | TC-09          |

### Why These Validations?
- **Status codes** catch broken endpoints and auth issues immediately
- **Body validation** catches data corruption and serialization bugs
- **Type checking** catches contract changes that could break consumers
- **Performance** catches regressions or infrastructure issues early
- **State verification** ensures CRUD operations have real effects

## Project Structure

```
api-test-framework/
├── config/
│   ├── __init__.py
│   └── settings.py              # API URLs, credentials, timeouts
├── models/
│   ├── __init__.py
│   └── booking.py               # Data models (dataclasses)
├── services/
│   ├── __init__.py
│   ├── base_client.py           # Reusable HTTP client with logging
│   └── booking_service.py       # Booking API operations
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Fixtures (service, auth, test data)
│   └── test_booking_api.py      # All test cases
├── utils/
│   ├── __init__.py
│   ├── test_data.py             # Test data factories
│   └── validators.py            # Reusable assertion helpers
├── pytest.ini                   # Pytest configuration
├── requirements.txt             # Python dependencies
└── README.md
```

## Framework Design

### Architecture: Service Layer Pattern

```
Tests → Services → Base Client → HTTP (requests)
  ↑         ↑           ↑
Models   Validators  Config
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **BaseAPIClient** | All HTTP logic (logging, sessions, timeouts) in one place — DRY |
| **Service classes** | Endpoint-specific methods; tests don't know about URLs or HTTP details |
| **Data models** (dataclasses) | Type-safe, reusable payloads; clean test code |
| **Test data factories** | Generate valid/invalid data without hardcoding in tests |
| **Validator helpers** | Consistent assertions across tests; readable error messages |
| **Session-scoped fixtures** | Reuse HTTP connections and auth tokens for performance |
| **pytest.parametrize** | Maximize coverage with minimal code duplication |

### Adding New Tests
1. Create test methods in existing test classes, or add a new test file in `tests/`
2. Use `booking_service` fixture for API calls
3. Use `utils/validators.py` for assertions
4. Use `utils/test_data.py` for test data generation

### Adding a New API Service
1. Create `services/new_service.py` inheriting from `BaseAPIClient`
2. Create `models/new_model.py` for data models
3. Add fixtures in `conftest.py`
4. Write tests in `tests/test_new_service.py`

## Setup & Run

### Prerequisites
- Python 3.9+

### Installation
```bash
git clone <repo-url>
cd api-test-framework
pip install -r requirements.txt
```

### Run Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test class
pytest tests/test_booking_api.py::TestCreateBooking

# Run only parametrized tests
pytest -k "various_data"
```

## Technologies
- **Python 3.9+**
- **pytest** — Test runner, fixtures, parametrize
- **requests** — HTTP client library
- **pytest-html** — HTML test reports
