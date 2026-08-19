import time

import pytest, yaml, os
from pathlib import Path

from helpers.api_client import ApiClient

@pytest.fixture(scope="session")
def config():
    """Load project configuration from YAML file."""
    config_path = Path(__file__).parent.parent / "config" / "env.yaml"

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    # CI runners have no display, so headless must be forceable without
    # editing env.yaml (which stays headless:false for local debugging).
    headless_env = os.getenv("HEADLESS")
    if headless_env is not None:
        cfg["headless"] = headless_env.lower() == "true"

    return cfg

@pytest.fixture(scope="session")
def credentials():
    """Load credentials from env or local YAML file."""

    # 1. Try environment variables first (CI/CD)
    email = os.getenv("TEST_EMAIL")
    password = os.getenv("TEST_PASSWORD")
    name = os.getenv("TEST_NAME")

    if email and password and name:
        return {
            "email": email,
            "password": password,
            "name": name
        }

    # Bug fix: previously, if only SOME of the three env vars were set (e.g.
    # CI defines TEST_EMAIL/TEST_PASSWORD as secrets but not TEST_NAME), the
    # code silently fell through to config/credentials.yaml — a gitignored
    # file that doesn't exist in CI — producing a confusing FileNotFoundError
    # instead of pointing at the actual misconfiguration.
    if email or password or name:
        missing = [
            var_name
            for var_name, value in [
                ("TEST_EMAIL", email),
                ("TEST_PASSWORD", password),
                ("TEST_NAME", name),
            ]
            if not value
        ]
        raise RuntimeError(
            "Partial TEST_* environment variables set; missing: "
            f"{', '.join(missing)}. Set all three or none."
        )

    # 2. Fallback to local file (only when no env vars were provided at all)
    credentials_path = Path(__file__).parent.parent / "config" / "credentials.yaml"

    with open(credentials_path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def api_client(config):
    return ApiClient(config["base_url"])


@pytest.fixture
def unique_email():
    """A throwaway email unlikely to collide with real accounts on the live site."""
    return f"qa_signup_{int(time.time() * 1000)}@example.com"


def required_account_fields(email: str, password: str = "TempPass123") -> dict:
    """Fields required by POST /api/createAccount, excluding the optional
    company/address2 (REQ-004 — tests should be able to omit them)."""
    return {
        "name": "QA Signup",
        "email": email,
        "password": password,
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "1",
        "birth_year": "1990",
        "firstname": "QA",
        "lastname": "Signup",
        "address1": "1 Test Street",
        "country": "India",
        "zipcode": "12345",
        "state": "Test State",
        "city": "Test City",
        "mobile_number": "1234567890",
    }


@pytest.fixture
def registered_account(api_client, unique_email):
    """Creates a real account via the API and deletes it after the test —
    used by tests that need an *already-registered* email to act against
    (e.g. the duplicate-email case, from either the API or the UI)."""
    fields = required_account_fields(unique_email)
    api_client.create_account(**fields)

    yield fields

    api_client.delete_account(email=fields["email"], password=fields["password"])