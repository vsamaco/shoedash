import pandas as pd
import streamlit as st

from processors.shoe_processor import ShoeProcessor


class ShoeTableComponent():
    def __init__(self, df_shoes: pd.DataFrame):
        self.shoe_processor = ShoeProcessor(df_shoes)
        self.column_config = {
            'gear_id': st.column_config.TextColumn('id'),
            'total_distance_mi': st.column_config.NumberColumn('Distance (mi)', format='%.2f mi'),
        }

    def render(self):
        shoes = self.shoe_processor.get_dataframe()
        st.dataframe(shoes, column_config=self.column_config)
