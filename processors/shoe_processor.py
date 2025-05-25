import pandas as pd


class ShoeProcessor():
    def __init__(self, df_shoes: pd.DataFrame):
        self.df = df_shoes.copy()

    def get_dataframe(self):
        return self.df

    def get_shoe_name_list(self):
        return sorted(self.df['name'].unique().tolist())

    def merge_retired_shoes(self, df_shoes):
        self.df = pd.concat([self.df, df_shoes], ignore_index=True)

        return self

    def merge_activities(self, df_activities):
        group_activities = df_activities.groupby(
            'name_shoe', as_index=False)['distance_mi'].sum()
        self.df = self.df.merge(
            group_activities, how='left', left_on='name', right_on='name_shoe')
        self.df['distance_mi'] = self.df['distance_mi'].fillna(
            0)

        activity_counts = df_activities['name_shoe'].value_counts(
        ).rename_axis('name_shoe').reset_index()
        activity_counts.columns = ['name_shoe', 'activity_count']
        self.df = self.df.merge(
            activity_counts, how='left', left_on='name', right_on='name_shoe')
        self.df['activity_count'] = self.df['activity_count'].fillna(
            0).astype(int)

        return self

    def filter_shoes_by_name(self, shoe_names):
        if len(shoe_names) > 0:
            self.df = self.df[self.df['name'].isin(shoe_names)]
        return self
