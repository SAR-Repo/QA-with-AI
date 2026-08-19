import requests


class ApiClient:
    """Thin wrapper around automationexercise.com's public REST API."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def create_account(self, **fields) -> requests.Response:
        """POST /api/createAccount. See https://automationexercise.com/api_list (API 11)."""
        return requests.post(f"{self.base_url}/api/createAccount", data=fields)

    def delete_account(self, email: str, password: str) -> requests.Response:
        """DELETE /api/deleteAccount. See https://automationexercise.com/api_list (API 12)."""
        return requests.delete(
            f"{self.base_url}/api/deleteAccount",
            data={"email": email, "password": password},
        )
