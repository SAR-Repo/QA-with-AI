import pytest, yaml, os
from pathlib import Path

@pytest.fixture(scope="session")
def config():
    """Load project configuration from YAML file."""
    config_path = Path(__file__).parent.parent / "config" / "env.yaml"

    with open(config_path) as f:
        return yaml.safe_load(f)

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