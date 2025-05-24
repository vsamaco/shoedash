import pandas as pd
import streamlit as st
import plotly.express as px
from processors.activity_processor import ActivityProcessor


class WeeklyActivitiesComponent():
    def __init__(self, df_activities: pd.DataFrame):
        self.activity_processor = ActivityProcessor(df_activities)

    def render(self):
        weekly_activities = self.activity_processor.filter_by_week_range(
            7).get_dataframe()

        weekly_activities['rolling_avg'] = weekly_activities['distance_mi'].rolling(
            window=8, min_periods=1).mean()

        grouped_df = weekly_activities.groupby(
            ['week_start', 'name_shoe'])['distance_mi'].sum().reset_index()

        weekly_fig = px.bar(grouped_df,
                            height=300,
                            x='week_start',
                            y='distance_mi',
                            color='name_shoe',
                            labels={'week_start': '', 'distance_mi': ""})
        weekly_fig.update_layout(showlegend=False)

        with st.container(border=True):
            st.plotly_chart(weekly_fig)
