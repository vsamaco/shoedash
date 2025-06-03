import streamlit as st
import plotly.express as px

from processors.activity_processor import ActivityProcessor


class ActivityDistanceCohortComponent():
    def __init__(self, df_activities):
        self.activity_processor = ActivityProcessor(df_activities)

    def render(self):
        cohort_counts = self.activity_processor.get_distance_cohort()
        fig = px.bar(
            cohort_counts,
            x='Distance (mi)',
            y='Activity Count',
            labels={
                'Activity Count': "Number of Activities",
            }
        )

        fig.update_layout(
            xaxis_title="Distance (mi)",
            yaxis_title="Number of Activities",
            bargap=0.1
        )

        config = {
            'toImageButtonOptions': {
                'filename': 'activity_distance_cohort',
            }
        }

        st.plotly_chart(fig, config=config)
