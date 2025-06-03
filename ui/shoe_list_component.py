import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from processors.activity_processor import ActivityProcessor
from processors.shoe_processor import ShoeProcessor


class ShoeListComponent():
    def __init__(self, df_shoes, df_activities):
        self.shoe_processor = ShoeProcessor(df_shoes)
        self.activity_processor = ActivityProcessor(df_activities)

    def _render_shoe_card(self, shoe: pd.Series, shoe_activities: pd.DataFrame):
        shoe_name = shoe['name']

        if shoe['retired']:
            shoe_name = f"🪦 {shoe_name}"
        shoe_total_miles = shoe['total_distance_mi']
        num_activities = len(
            shoe_activities) if not shoe_activities.empty else None
        activity_miles = shoe_activities['distance_mi'].mean(
        ) if not shoe_activities.empty else None

        st.subheader(shoe_name, divider=True)
        col1, col2, col3 = st.columns(3)
        col1.metric('Total Miles', f"{round(shoe_total_miles)} mi")
        if not shoe_activities.empty:
            col2.metric(
                'Activities', f"{num_activities}")
        if not shoe_activities.empty:
            col3.metric('Average Miles',
                        f"{activity_miles:.1f} mi")

    def _render_shoe_activities(self, shoe_activities: pd.DataFrame):
        st.dataframe(shoe_activities[['start_date_local', 'name', 'distance_mi']],
                     height=200,
                     column_config={
                         'start_date_local': st.column_config.DateColumn('date', format='M/DD/YYYY'),
                         'distance_mi': st.column_config.NumberColumn('distance (mi)', format="%.2f mi")
        })

    def _render_shoe_activity_chart(self, shoe, shoe_activities: pd.DataFrame, start_date, end_date, num_activities):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=shoe_activities['start_date_local'],
            y=shoe_activities['distance_mi'],
            width=[0.8] * num_activities,
        ))

        fig.update_layout(
            height=300,
            xaxis_range=(start_date, end_date),
            xaxis_title='Date',
            yaxis_title='Distance (mi)',
            bargap=0.2,
        )

        config = {
            'toImageButtonOptions': {
                'filename': f"{shoe['name'].replace(' ', '_')}_shoe_distance_chart",
            }
        }

        st.plotly_chart(fig, config=config)

    def _render_distance_cohort_chart(self, gear_id):
        cohort_counts = self.activity_processor.get_distance_cohort(
            gear_id=gear_id)
        fig = px.bar(
            cohort_counts,
            x='Distance (mi)',
            y='Activity Count',
            labels={
                'Activity Count': "Number of Activities",
            },
            height=300,
        )

        fig.update_layout(
            xaxis_title="Distance (mi)",
            yaxis_title="Number of Activities",
            bargap=0.1,
        )

        config = {
            'toImageButtonOptions': {
                'filename': 'shoe_activity_distance_cohort',
            }
        }

        st.plotly_chart(fig, config=config)

    def render(self):
        shoes = self.shoe_processor.get_dataframe()
        activities = self.activity_processor.get_dataframe()
        start_date = activities['start_date_local'].min()
        end_date = activities['start_date_local'].max()

        shoe_map = {}
        for index, shoe in shoes.iterrows():
            shoe_label = shoe['name']
            if shoe['retired']:
                shoe_label = f'🪦 {shoe_label}'
            shoe_map[index] = shoe_label

        shoe_selected_pill = st.pills(
            'Select Shoe', options=shoe_map.keys(), format_func=lambda option: shoe_map[int(option)], default=list(shoe_map.keys())[0] if len(shoe_map) else None, label_visibility='hidden')

        for index, shoe in shoes.iterrows():
            if shoe_selected_pill != index:
                continue
            shoe_activities = activities[activities['name_shoe']
                                         == shoe['name']].reset_index()
            shoe_activities.index = range(1, len(shoe_activities) + 1)

            with st.container(border=True):
                self._render_shoe_card(shoe, shoe_activities)
                tab1, tab2, tab3 = st.tabs(
                    ['Activities', 'Activity Chart', 'Distance Cohorts'])
                with tab1:
                    if not shoe_activities.empty:
                        self._render_shoe_activities(shoe_activities)

                with tab2:
                    if not shoe_activities.empty:
                        self._render_shoe_activity_chart(
                            shoe, shoe_activities, start_date, end_date, len(activities))
                with tab3:
                    if not shoe_activities.empty:
                        self._render_distance_cohort_chart(shoe['gear_id'])
