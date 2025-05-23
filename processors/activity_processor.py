from datetime import timedelta
import pandas as pd


class ActivityProcessor():
    def __init__(self, df_activities):
        self.original_df = df_activities
        self.df = self.original_df.copy()

    def reset(self):
        self.df = self.original_df
        return self.df

    def filter_by_week_range(self, weeks_ago):
        # assign week start to Monday 00:00
        self.df['week_start'] = self.df['start_date_local'].dt.to_period(
            'W').apply(lambda r: r.start_time)

        # most recent week
        end_week = self.df['week_start'].max()
        start_week = end_week - timedelta(weeks=weeks_ago)

        # filter
        self.df = self.df[self.df['week_start'] >= start_week].copy()

        return self

    def get_dataframe(self):
        return self.df

    def merge_with_shoes(self, shoes_df):
        self.df = pd.merge(self.df, shoes_df, on='gear_id',
                           how='inner', suffixes=('', '_shoe'))
        return self

    def filter_by_year_range(self, start_year, end_year):
        '''Filters activities between start and end year inclusive'''
        if end_year < start_year:
            return self

        self.df = self.df[self.df['start_date_local'].dt.year.between(
            start_year, end_year)]
        return self

    def filter_by_shoes(self, shoe_ids):
        '''Filters activities with matching shoes from shoe_list'''
        self.df = self.df[self.df['gear_id']].isin(shoe_ids)
        return self.df

    def get_activities_years(self):
        return sorted(self.df['start_date_local'].dt.year.dropna().unique())
