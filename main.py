import os
import requests
import streamlit as st
from dotenv import load_dotenv

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

# ====== GET DATA ======= #


@st.cache_data
def get_profile():
    response = requests.get(DEMO_PROFILE_URL, timeout=1000)
    if response.status_code != 200:
        st.error('Fetch profile error')
        st.stop()

    return response.json()


@st.cache_data
def get_activities():
    response = requests.get(DEMO_ACTIVITY_URL, timeout=1000)
    if response.status_code != 200:
        st.error('Fetch activities error')
        st.stop()

    return response.json()


profile_data = get_profile()
shoe_processor = ShoeProcessor(profile_data)
df_shoes = shoe_processor.get_dataframe()

activities_data = get_activities()
activity_processor = ActivityProcessor(activities_data)
df_activities = activity_processor.merge_with_shoes(df_shoes).get_dataframe()

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
