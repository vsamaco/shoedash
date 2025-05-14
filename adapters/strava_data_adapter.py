from adapters.base_data_adapter import BaseDataAdapter
from lib.strava import Strava


class StravaDataAdapter(BaseDataAdapter):
    def __init__(self, strava: Strava):
        self.strava = strava

    def get_athlete(self, athlete_id):
        return self.strava.get_athlete()

    def get_activities(self, athlete_id):
        return self.strava.get_activities()
