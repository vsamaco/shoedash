import pandas as pd
import plotly.express as px
import streamlit as st
from processors.activity_processor import ActivityProcessor


class WeekDistanceYearlyChartComponent():
    def __init__(self, df_activities):
        self.activity_processor = ActivityProcessor(df_activities)

    def render(self):
        df_weekly = self.activity_processor.get_weekly_distance_per_year()

        fig = px.line(
            df_weekly,
            x="normalized_week",
            y="distance_mi",
            color='year_start',
            markers=True,
            labels={
                'normalized_week': 'Week Date',
                'distance_mi': 'Distance (mi)',
                'year_start': 'Year'
            }
        )

        fig.update_layout(
            xaxis=dict(
                tickformat="%b %d",
                range=[pd.Timestamp("2000-01-01"), pd.Timestamp("2000-12-31")]
            )
        )
        st.subheader('Weekly Distance Per Year', divider=True)
        st.plotly_chart(fig)
