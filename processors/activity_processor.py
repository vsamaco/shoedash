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
        self.df['week_start'] = self.df['start_date_local'] - \
            pd.to_timedelta(self.df['start_date_local'].dt.weekday, unit='D')
        self.df['week_start'] = self.df['week_start'].dt.normalize()

        # most recent week
        end_week = self.df['week_start'].max()
        start_week = end_week - timedelta(weeks=weeks_ago)

        # filter
        self.df = self.df[self.df['week_start'] >= start_week].copy()

        return self

    def get_dataframe(self):
        return self.df

    def get_weekly_distance_per_year(self):
        df_activities = self.get_dataframe().copy()
        df_activities['week_start'] = df_activities['start_date_local'] - \
            pd.to_timedelta(
                df_activities['start_date_local'].dt.weekday, unit='D')
        df_activities['week_start'] = df_activities['week_start'].dt.normalize()
        df_activities['year_start'] = df_activities['week_start'].dt.year

        df_activities['normalized_week'] = df_activities['week_start'].apply(
            lambda d: d.replace(year=2000))

        df_weekly = df_activities.groupby(
            ['year_start', 'normalized_week'])['distance_mi'].sum().reset_index()

        return df_weekly

    def get_monthly_distance_per_year(self):
        df_activities = self.get_dataframe().copy()
        df_activities['month_start'] = df_activities['start_date_local'].dt.month
        df_activities['year_start'] = df_activities['start_date_local'].dt.year

        df_monthly = df_activities.groupby(
            ['year_start', 'month_start'], sort=False)['distance_mi'].sum().reset_index()
        df_monthly['month_name'] = df_monthly['month_start'].apply(
            lambda m: pd.to_datetime(f'2025-{m}-01').strftime('%b'))

        return df_monthly

    def merge_with_shoes(self, shoes_df):
        self.df = pd.merge(self.df, shoes_df,
                           how='left', left_on='gear_id', right_on='gear_id', suffixes=('', '_shoe'))
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

    def merge_missing_shoes(self, df_shoes):
        self.df = self.df.merge(
            df_shoes[['gear_id', 'name']], how='left', on='gear_id')

        return self

    def get_activities_years(self):
        return sorted(self.df['start_date_local'].dt.year.dropna().unique())

    def get_missing_gear_ids(self, df_shoes: pd.DataFrame):
        # Get gear ids from activities
        activity_gear_ids = self.df["gear_id"].dropna().unique()

        # Get gear ids from shoes
        shoe_ids = df_shoes["gear_id"].unique()

        # Get gear_ids that are in activities but not in shoes
        missing_gear_ids = list(set(activity_gear_ids) - set(shoe_ids))

        return missing_gear_ids
