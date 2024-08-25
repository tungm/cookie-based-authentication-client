import requests
from lxml import etree

from .WebUtilities import WebUtilities

class CookieBasedAuthenticationService:

    def __init__(self, base_url: str, login_page_path: str, login_path: str, username: str, password: str):
        """
        Initializes a new instance of the CookieBasedAuthenticationService class.

        Args:
            base_url (str): The base URL of the authentication service.
            login_page_path (str): The path to the login page.
            login_path (str): The path to the login endpoint.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        self.base_url = base_url
        self.login_page_path = login_page_path
        self.login_path = login_path
        self.username = username
        self.password = password
        self.session = requests.Session()
        self._login(username, password)

    def _post(self, path: str, data):
        """
        Sends a POST request to the specified path with the given data.

        Args:
            path (str): The path to send the request to.
            data (dict): The data to include in the request.

        Returns:
            requests.Response: The response from the server.
        """
        # TODO: Add common headers, body message to the request
        response = self.session.post(f"{self.base_url}/{path}", data=data)
        if response.status_code == 401:
            self._login(self.username, self.password)
            response = self.session.post(f"{self.base_url}/{path}", data=data)
        return response

    def _login(self, username: str, password: str) -> bool:
        """
        Logs in to the authentication service with the specified username and password.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.

        Returns:
            bool: True if the login was successful, False otherwise.
        """
        login_url = f"{self.base_url}/{self.login_path}"
        login_data = {
            'username': username,
            'password': password,
            '_csrf': self._get_csrf_token()
        }
        response = self.session.post(login_url, data=login_data)
        return response.status_code == 200
    
    def _get_csrf_token(self) -> str:
        """
        Retrieves the CSRF token from the login page.

        Returns:
            str: The CSRF token.
        """
        login_page = WebUtilities.get_page_content(f"{self.base_url}/{self.login_page_path}")
        csrf_token = WebUtilities.get_elements_by_xpath(login_page, '//input[@name="_csrf"]/@value')[0]
        return csrf_token
