import time
from adapters.base_data_adapter import BaseDataAdapter
from lib.strava import Strava


class StravaDataAdapter(BaseDataAdapter):
    def __init__(self, strava: Strava):
        self.strava = strava

    def get_athlete(self, athlete_id):
        return self.strava.get_athlete()

    def get_activities(self, athlete_id, per_page, page):
        activities = []
        for i in range(1, page+1):
            page_activities = self.strava.get_activities(
                per_page=per_page, page=i)

            if len(page_activities) == 0:
                break
            activities.extend(page_activities)

        return activities
