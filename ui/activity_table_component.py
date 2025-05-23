import pandas as pd
import streamlit as st

from processors.activity_processor import ActivityProcessor


class ActivityTableComponent():
    def __init__(self, df_activities: pd.DataFrame):
        self.activity_processor = ActivityProcessor(df_activities)
        self.column_config = {
            'start_date_local': st.column_config.DatetimeColumn('Start Date', format='YYYY-MM-DD'),
            'distance_mi': st.column_config.NumberColumn('Distance (mi)', format='%.2f mi'),
            'gear_id': st.column_config.TextColumn('Gear ID'),
            'name_shoe': st.column_config.TextColumn('Shoe'),
            'total_distance_mi': None,
            'retired': None,
        }

    def render(self):
        activities = self.activity_processor.get_dataframe()
        st.dataframe(activities, column_config=self.column_config)
