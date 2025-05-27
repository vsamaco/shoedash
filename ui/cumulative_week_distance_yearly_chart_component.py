import streamlit as st
import plotly.express as px
from processors.activity_processor import ActivityProcessor


class CumulativeDistanceYearlyChartComponent():
    def __init__(self, df_activities):
        self.activity_processor = ActivityProcessor(df_activities)

    def render(self):
        weekly_df = self.activity_processor.get_weekly_distance_per_year()
        weekly_df['cumulative_distance_mi'] = weekly_df.groupby('year_start')[
            'distance_mi'].cumsum()

        fig = px.line(
            weekly_df,
            x='normalized_week',
            y='cumulative_distance_mi',
            color='year_start',
            markers=True,
            labels={
                'normalized_week': 'Week Date',
                'cumulative_distance_mi': 'Distance (mi)',
                'year_start': 'Year'
            },
            hover_data={
                'cumulative_distance_mi': ':.2f'
            },
        )

        fig.update_layout(
            xaxis=dict(tickformat="%b %d"),
            yaxis_title="Cumulative Distance (mi)",
            legend_title="Year",
        )
        config = {
            'toImageButtonOptions': {
                'filename': 'cumulative_week_distance_yearly_chart',
            }
        }

        st.subheader('Cumulative Week Distance Per Year', divider=True)
        st.plotly_chart(fig, config=config)
