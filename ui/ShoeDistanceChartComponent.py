import plotly.express as px
import streamlit as st


class ShoeDistanceChartComponent():
    def __init__(self, df_shoe_distance_cumulative):
        self.df_shoe_distance_cumulative = df_shoe_distance_cumulative

    def render(self):
        fig = px.line(
            self.df_shoe_distance_cumulative,
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
