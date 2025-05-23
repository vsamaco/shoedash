import os
import streamlit as st
from dotenv import load_dotenv
from adapters.base_data_adapter import get_activities, get_athlete
from adapters.demo_data_adapter import DemoDataAdapter
from adapters.strava_data_adapter import StravaDataAdapter
from lib.strava import Strava
from lib.strava_auth_manager import StravaAuthManager
from processors.activity_processor import ActivityProcessor
from processors.shoe_processor import ShoeProcessor
from repositories.activity_repository import ActivityRepository
from repositories.athlete_repository import AthleteRepository
from ui.activity_table_component import ActivityTableComponent
from ui.shoe_distance_chart_component import ShoeDistanceChartComponent
from ui.shoe_list_component import ShoeListComponent
from ui.shoe_table_component import ShoeTableComponent
from ui.overview_stats_component import OverviewStatsComponent
from ui.weekly_activities_component import WeeklyActivitiesComponent

load_dotenv(override=True)

st.set_page_config(page_title="Shoe Dashboard", page_icon="👟")

# ====== CONFIG ====== #

CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('STRAVA_REDIRECT_URI')

if "mode" not in st.session_state:
    st.session_state.mode = 'demo'

if "strava" not in st.session_state:
    st.session_state.strava = Strava(
        CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope="profile:read_all,activity:read")

# ======  AUTH ======= #

strava = st.session_state.strava
auth = StravaAuthManager(strava)
auth.handle_auth(st.session_state.mode)

with st.sidebar:
    def update_mode():
        st.session_state.mode = st.session_state.selected_mode

    source_values = ['demo', 'strava']
    st.selectbox('Source', ['demo', 'strava'],
                 index=source_values.index(st.session_state.mode), on_change=update_mode, key='selected_mode')
    page = st.number_input("Source pages", min_value=1,
                           max_value=10) if st.session_state.mode == 'strava' else 1

# ====== GET DATA ======= #
mode = st.session_state.mode
athlete_id = st.session_state.strava.athlete.get('id')
data_adapter = StravaDataAdapter(strava
                                 ) if st.session_state.mode == 'strava' else DemoDataAdapter()
athlete_repository = AthleteRepository(get_athlete(data_adapter, mode,
                                                   athlete_id))

activity_repository = ActivityRepository(get_activities(
    data_adapter, mode, athlete_id, page))

activity_processor = ActivityProcessor(activity_repository.get_activities_df())
activity_year_values = activity_processor.get_activities_years()

shoe_processor = ShoeProcessor(athlete_repository.get_shoes_df())
available_shoes = shoe_processor.get_shoe_name_list()


with st.sidebar:
    activity_start_year = st.selectbox(
        'Start Year', activity_year_values, index=0)
    activity_end_year = st.selectbox(
        'End Year',
        activity_year_values,
        index=len(activity_year_values) - 1,
    )

    selected_shoes = st.multiselect(
        "Select Shoes",
        options=available_shoes)


df_shoes = shoe_processor.filter_shoes_by_name(selected_shoes).get_dataframe()
df_activities = activity_processor.filter_by_year_range(
    activity_start_year, activity_end_year).merge_with_shoes(df_shoes).get_dataframe()

athlete = athlete_repository.get_profile()

# ====  BUILD UI ==== #


def main():
    st.title("Shoe Dashboard")
    st.subheader(f"Hello {athlete.get('firstname')}")

    st.subheader("Overview")
    OverviewStatsComponent(df_activities, df_shoes).render()

    st.subheader('Weekly Mileage')
    WeeklyActivitiesComponent(df_activities).render()

    st.subheader(f'Shoes ({len(df_shoes)})')
    ShoeListComponent(df_shoes, df_activities).render()

    st.subheader('Overall Data')
    tab1, tab2, tab3 = st.tabs(['Activities', 'Shoes', 'All-time Distance'])
    with tab1:
        ActivityTableComponent(df_activities).render()
    with tab2:
        ShoeTableComponent(df_shoes, df_activities).render()
    with tab3:
        ShoeDistanceChartComponent(df_activities).render()


main()
