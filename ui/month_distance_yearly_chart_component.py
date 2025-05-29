import streamlit as st
import plotly.express as px
from processors.activity_processor import ActivityProcessor


class MonthDistanceYearlyChartComponent():
    def __init__(self, df_activities):
        self.activity_processor = ActivityProcessor(df_activities)

    def render(self):
        df_monthly = self.activity_processor.get_monthly_distance_per_year()
        fig = px.line(
            df_monthly,
            x="month_name",
            y="distance_mi",
            color='year_start',
            markers=True,
            labels={
                'month_name': 'Date',
                'distance_mi': 'Distance (mi)',
                'year_start': 'Year'
            },
            hover_data={
                'distance_mi': ':.2f'
            },
        )
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                       'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        fig.update_layout(
            xaxis=dict(
                categoryorder='array', categoryarray=month_order,
            ),
        )

        config = {
            'toImageButtonOptions': {
                'filename': 'month_distance_yearly_chart',
            }
        }

        st.subheader('Monthly Distance Per Year', divider=True)
        st.plotly_chart(fig, config=config)
