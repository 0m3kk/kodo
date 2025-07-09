from typing import Optional
import requests


class APIFetchTools:
    """
    A class for fetching data from APIs.
    """

    def __init__(self):
        """Initializes the APIFetchTools."""
        pass

    def fetch_api_data(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> str:
        """
        Fetches data from a given API endpoint.

        Args:
            url: The URL of the API endpoint.
            method: The HTTP method to use (GET, POST, PUT, DELETE, etc.). Defaults to GET.
            headers: A dictionary of HTTP headers to send with the request.
            data: A dictionary of data to send in the request body (for POST, PUT, etc.).
            limit: The maximum number of characters to return.
            offset: The number of characters to skip before starting to collect the result set.

        Returns:
            The response from the API as a string, or an error message.
        """
        try:
            if headers is not None and len(headers) == 0:
                headers = None
            if data is not None and len(data) == 0:
                data = None

            response = requests.request(method, url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            content = response.text

            if offset is not None:
                content = content[offset:]
            if limit is not None:
                content = content[:limit]

            return content
        except requests.exceptions.RequestException as e:
            return f"Error fetching API data from {url}: {e}"
