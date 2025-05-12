import streamlit as st


class ShoeTableComponent():
    def __init__(self, df_shoes):
        self.df_shoes = df_shoes
        self.column_config = {
            'gear_id': st.column_config.TextColumn('id'),
            'total_distance_mi': st.column_config.NumberColumn('Distance (mi)', format='%.2f mi'),
        }

    def render(self):
        st.dataframe(self.df_shoes, column_config=self.column_config)
