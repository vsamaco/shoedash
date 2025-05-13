import requests
import time
from urllib.parse import urlencode


class Strava():
    BASE_URL = 'https://www.strava.com/api/v3'
    AUTH_URL = f"{BASE_URL}/oauth/authorize"
    TOKEN_URL = f"{BASE_URL}/oauth/token"

    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        self.athlete = {}

    def get_login_url(self):
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": self.scope,
            "approval_prompt": "auto",
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"

    def request_access_token(self, code):
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
        }
        response = requests.post(
            self.TOKEN_URL,
            data=params,
            timeout=1000,
        )
        if response.status_code == 200:
            self._update_tokens(response.json())
            return True
        return False

    def refresh_access_token(self):
        if not self.refresh_token:
            raise ValueError('refresh token required')

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        response = requests.post(
            self.TOKEN_URL,
            data=data,
            timeout=1000,
        )
        if response.status_code == 200:
            self._update_tokens(response.json())
            return True
        return False

    def _check_valid_token(self):
        if self.expires_at is None or time.time() >= self.expires_at:
            self.refresh_access_token()

    def _update_tokens(self, data):
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.expires_at = data['expires_at']
        self.athlete = data.get('athlete', {})

    def get(self, endpoint, params=None):
        self._check_valid_token()

        headers = {'Authorization': f"Bearer {self.access_token}"}
        response = requests.get(
            f"{self.BASE_URL}/{endpoint}", headers=headers, params=params, timeout=5000)
        response.raise_for_status()
        return response.json()

    def get_activities(self, per_page=25, page=1):
        return self.get('athlete/activities', params={"per_page": per_page, "page": page})

    def get_athlete(self):
        return self.get('athlete')

    def get_gear(self, gear_id):
        return self.get(f'gear/{gear_id}')
