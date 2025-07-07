from typing import Optional
import requests

class APIFetchTools:
    """
    A class for fetching data from APIs.
    """

    def __init__(self):
        """Initializes the APIFetchTools."""
        pass

    def fetch_api_data(self, url: str, method: str = "GET", headers: Optional[dict] = None, data: Optional[dict] = None) -> str:
        """
        Fetches data from a given API endpoint.

        Args:
            url: The URL of the API endpoint.
            method: The HTTP method to use (GET, POST, PUT, DELETE, etc.). Defaults to GET.
            headers: A dictionary of HTTP headers to send with the request.
            data: A dictionary of data to send in the request body (for POST, PUT, etc.).

        Returns:
            The response from the API as a string, or an error message.
        """
        try:
            response = requests.request(method, url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            return f"Error fetching API data from {url}: {e}"
