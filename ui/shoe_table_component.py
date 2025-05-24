import pandas as pd
import streamlit as st

from processors.activity_processor import ActivityProcessor
from processors.shoe_processor import ShoeProcessor


class ShoeTableComponent():
    def __init__(self, df_shoes: pd.DataFrame, df_activities):
        self.shoe_processor = ShoeProcessor(df_shoes)
        self.activity_processor = ActivityProcessor(df_activities)
        self.column_config = {
            'name': st.column_config.TextColumn('Shoe'),
            'activity_count': st.column_config.NumberColumn('Activities'),
            'total_distance_mi': st.column_config.NumberColumn('Distance (mi)', format='%.2f mi'),
            'distance_mi': st.column_config.NumberColumn('Activity Distance (mi)', format='%.2f mi')
        }

    def render(self):
        activities = self.activity_processor.get_dataframe()
        shoes = self.shoe_processor.merge_activities(
            activities).get_dataframe()
        shoes.index = pd.RangeIndex(start=1, stop=len(shoes) + 1)

        shoes = shoes[['name', 'activity_count',
                       'distance_mi', 'total_distance_mi']]
        st.dataframe(shoes, column_config=self.column_config)
