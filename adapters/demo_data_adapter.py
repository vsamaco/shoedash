import os

import requests
from adapters.base_data_adapter import BaseDataAdapter


class DemoDataAdapter(BaseDataAdapter):
    MODE = "demo"
    DEMO_PROFILE_URL = os.environ.get('DEMO_PROFILE_URL', '')
    DEMO_ACTIVITY_URL = os.environ.get('DEMO_ACTIVITY_URL', '')
    DEMO_GEAR_URL = os.environ.get('DEMO_GEAR_URL', '')
    TIMEOUT = 1000

    def get_mode(self):
        return self.MODE

    def get_athlete(self, athlete_id):
        response = requests.get(self.DEMO_PROFILE_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()

    def get_activities(self, athlete_id, per_page=100, page=1):
        response = requests.get(self.DEMO_ACTIVITY_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()

    def get_gear(self, gear_id):
        response = requests.get(self.DEMO_GEAR_URL, timeout=self.TIMEOUT)
        response.raise_for_status()

        all_gear = response.json()
        for gear in all_gear:
            if gear['id'] == gear_id:
                return gear
        return None
