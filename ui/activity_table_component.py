import pandas as pd
import streamlit as st

from processors.activity_processor import ActivityProcessor


class ActivityTableComponent():
    def __init__(self, df_activities: pd.DataFrame):
        self.activity_processor = ActivityProcessor(df_activities)
        self.column_config = {
            'name': st.column_config.TextColumn('Name'),
            'start_date_local': st.column_config.DatetimeColumn('Date', format='M/DD/YYYY'),
            'distance_mi': st.column_config.NumberColumn('Distance (mi)', format='%.2f mi'),
            'name_shoe': st.column_config.TextColumn('Shoe'),
        }

    def render(self):
        activities = self.activity_processor.get_dataframe()
        activities.index = pd.RangeIndex(1, len(activities) + 1)
        activities = activities[['start_date_local', 'name', 'distance_mi',
                                 'name_shoe']]
        st.dataframe(activities, column_config=self.column_config)
