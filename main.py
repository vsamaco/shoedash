import os
import requests
import streamlit as st
from dotenv import load_dotenv
from lib.strava import Strava
from lib.strava_auth_manager import StravaAuthManager
from processors.ActivityProcessor import ActivityProcessor
from processors.ShoeProcessor import ShoeProcessor
from ui.ActivityTableComponent import ActivityTableComponent
from ui.ShoeDistanceChartComponent import ShoeDistanceChartComponent
from ui.ShoeTableComponent import ShoeTableComponent

load_dotenv()

st.set_page_config(page_title="Shoe Dashboard", page_icon="👟")

# ====== CONFIG ====== #

CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('STRAVA_REDIRECT_URI')
DEMO_PROFILE_URL = os.environ.get('DEMO_PROFILE_URL', '')
DEMO_ACTIVITY_URL = os.environ.get('DEMO_ACTIVITY_URL', '')


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

# ====== GET DATA ======= #


@st.cache_data
def get_profile(mode, athlete_id=None):
    print(f'get profile: {mode}')
    if mode == "strava" and athlete_id:
        return strava.get_athlete()
    else:
        response = requests.get(DEMO_PROFILE_URL, timeout=1000)
        if response.status_code != 200:
            st.error('Fetch profile error')
            st.stop()

        return response.json()


@st.cache_data
def get_activities(mode, athlete_id=None):
    print(f'get activities: {mode}')
    if mode == 'strava' and athlete_id:
        return strava.get_activities(per_page=25, page=1)
    else:
        response = requests.get(DEMO_ACTIVITY_URL, timeout=1000)
        if response.status_code != 200:
            st.error('Fetch activities error')
            st.stop()

        return response.json()


profile_data = get_profile(st.session_state.mode,
                           st.session_state.strava.athlete.get('id'))
activities_data = get_activities(
    st.session_state.mode, st.session_state.strava.athlete.get('id'))

shoe_processor = ShoeProcessor(profile_data)
activity_processor = ActivityProcessor(activities_data)

activity_year_values = activity_processor.get_activities_years()
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
df_activities = activity_processor.merge_with_shoes(df_shoes).filter_by_year_range(
    activity_start_year, activity_end_year).get_dataframe()
df_cumulative_shoe_distance = activity_processor.get_cumulative_shoe_distance()

# ====  BUILD UI ==== #


def main():
    st.title("Shoe Dashboard")
    st.subheader(f"Hello {profile_data['firstname']}")

    st.subheader(f'Shoes ({len(df_shoes)})')
    ShoeTableComponent(df_shoes).render()

    st.subheader(f'Activities ({len(df_activities)})')
    ActivityTableComponent(df_activities).render()

    st.subheader("Stats")
    ShoeDistanceChartComponent(df_cumulative_shoe_distance).render()


main()
