import pandas as pd


class AthleteRepository():
    def __init__(self, athlete_data):
        self.athlete_data = athlete_data

    def get_profile(self):
        return self.athlete_data or {}

    def get_shoes_df(self):
        df = pd.DataFrame(self.athlete_data['shoes'])
        df.rename(columns={
                  'id': 'gear_id', 'converted_distance': 'total_distance_mi'}, inplace=True)

        return df[['gear_id', 'name', 'total_distance_mi', 'retired']]
