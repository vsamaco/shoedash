import pandas as pd

METERS_TO_MILES = 0.000621371


class ActivityRepository():
    def __init__(self, activities_json):
        self.activities_json = activities_json

    def get_activities_df(self):
        df = pd.DataFrame(self.activities_json)
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['start_date_local'] = pd.to_datetime(df['start_date_local'])

        df = df[df['sport_type'] == 'Run']
        df['distance_mi'] = df['distance'] * METERS_TO_MILES
        df.sort_values('start_date_local', inplace=True)

        return df[['id', 'start_date', 'start_date_local', 'name', 'distance_mi', 'gear_id']]
