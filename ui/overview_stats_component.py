import datetime as dt
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from processors.activity_processor import ActivityProcessor
from processors.shoe_processor import ShoeProcessor


class OverviewStatsComponent():
    def __init__(self, df_activities: pd.DataFrame, df_shoes: pd.DataFrame):
        self.activity_processor = ActivityProcessor(df_activities)
        self.shoe_processor = ShoeProcessor(df_shoes)

    def _render_num_activities(self, df_activities: pd.DataFrame):
        num_activities = len(df_activities)
        st.metric(label='Activities:', value=num_activities, border=True)

    def _render_num_shoes(self, df_shoes: pd.DataFrame):
        num_shoes = len(df_shoes)
        st.metric(label='Shoes:', value=num_shoes, border=True)

    def _render_total_shoe_mileage(self, df_activities: pd.DataFrame):
        total_mileage = df_activities['distance_mi'].sum()

        st.metric(label='Total Shoe Mileage',
                  value=f"{round(total_mileage)} mi", border=True)

    def _render_weekly_mileage(self, df_activities: pd.DataFrame):
        average_weekly_miles = df_activities.groupby(
            'week_start')['distance_mi'].sum().mean()
        st.metric(label='Weekly Mileage',
                  value=f" {round(average_weekly_miles)} mi",
                  border=True)

    def _render_dates(self, df_activities: pd.DataFrame):
        start_date = df_activities['start_date_local'].min().strftime(
            '%m/%d/%Y')

        end_date = df_activities['start_date_local'].max().strftime(
            '%m/%d/%Y')

        st.text(f"{start_date} - {end_date}")

    def render(self):
        df_shoes = self.shoe_processor.get_dataframe()
        df_activities = self.activity_processor.get_dataframe()
        df_recent_activities = self.activity_processor.filter_by_week_range(
            8).get_dataframe()

        self._render_dates(df_activities)

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        with col1:
            self._render_num_shoes(df_shoes)
        with col2:
            self._render_total_shoe_mileage(df_activities)
        with col3:
            self._render_num_activities(df_activities)
        with col4:
            self._render_weekly_mileage(df_recent_activities)
