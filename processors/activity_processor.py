from datetime import timedelta
import pandas as pd
import streamlit as st


class ActivityProcessor():
    def __init__(self, df_activities):
        self.original_df = df_activities
        self.df = self.original_df.copy()

    def reset(self):
        self.df = self.original_df
        return self.df

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

    def get_cumulative_shoe_distance(self):
        '''Returns dataframe with cumulative distance per shoe over time'''
        df = self.df.copy()
        df = df.sort_values(['name_shoe', 'start_date_local'])

        grouped = df.groupby(['name_shoe', 'start_date_local']).agg(
            {'distance_mi': 'sum'}).reset_index()

        grouped['cumulative_distance'] = grouped.groupby(
            'name_shoe')['distance_mi'].cumsum()
        return grouped
