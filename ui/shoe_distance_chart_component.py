import pandas as pd
import plotly.express as px
import streamlit as st

from processors.activity_processor import ActivityProcessor


class ShoeDistanceChartComponent():
    def __init__(self, df_activities: pd.DataFrame):
        self.activity_processor = ActivityProcessor(df_activities)

    def _get_culumative_shoe_distance(self):
        '''Returns dataframe with cumulative distance per shoe over time'''
        df = self.activity_processor.get_dataframe()
        st.write(df)
        df = df.sort_values(['name_shoe', 'start_date_local'])

        grouped = df.groupby(['name_shoe', 'start_date_local']).agg(
            {'distance_mi': 'sum'}).reset_index()

        grouped['cumulative_distance'] = grouped.groupby(
            'name_shoe')['distance_mi'].cumsum()
        return grouped

    def render(self):
        df_shoe_distance_cumulative = self._get_culumative_shoe_distance()
        fig = px.line(
            df_shoe_distance_cumulative,
            x="start_date_local",
            y="cumulative_distance",
            color="name_shoe",
            markers=True,
            labels={'start_date_local': 'Date', 'name_shoe': 'Shoe',
                    'cumulative_distance': 'Distance (mi)'}
        )
        fig.update_layout(
            xaxis=dict(
                tickformat="%m/%d/%y"  # e.g., 5/1/2024
            )
        )
        st.plotly_chart(fig)
