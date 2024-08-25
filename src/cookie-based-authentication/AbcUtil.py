from .CookieBasedAuthenticationService import CookieBasedAuthenticationService

class AbcUtil(CookieBasedAuthenticationService):

    LOGIN_PAGE_PATH = "login"
    LOGIN_PATH = "submit_login"

    def __init__(self, base_url, username, password):
        super().__init__(base_url, self.LOGIN_PAGE_PATH, self.LOGIN_PATH, username, password)

    def get_abc_by_id(self, abc_id):
        response = self._post(f"get_abc/{abc_id}", {})
        return response.json()
