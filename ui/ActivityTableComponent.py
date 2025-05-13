import streamlit as st


class ActivityTableComponent():
    def __init__(self, df_activities):
        self.df_activities = df_activities
        self.column_config = {
            'start_date_local': st.column_config.DatetimeColumn('Start Date', format='YYYY-MM-DD'),
            'distance_mi': st.column_config.NumberColumn('Distance (mi)', format='%.2f mi'),
            'gear_id': st.column_config.TextColumn('Gear ID'),
            'name_shoe': st.column_config.TextColumn('Shoe'),
            'total_distance_mi': None,
            'retired': None,
        }

    def render(self):
        st.dataframe(self.df_activities, column_config=self.column_config)
