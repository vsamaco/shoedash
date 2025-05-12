import pandas as pd


class ShoeProcessor():
    def __init__(self, profile_json):
        self.shoes = profile_json['shoes']
        self.original_df = self._to_dataframe()
        self.df = self.original_df.copy()

    def _to_dataframe(self):
        df = pd.DataFrame(self.shoes)
        df.rename(columns={
                  'id': 'gear_id', 'converted_distance': 'total_distance_mi'}, inplace=True)
        return df[['gear_id', 'name', 'total_distance_mi', 'retired']]

    def get_dataframe(self):
        return self.df
