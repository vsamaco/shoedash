import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Shoe Dashboard", page_icon="👟")

CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('STRAVA_REDIRECT_URI')
DEMO_PROFILE_URL = os.environ.get('DEMO_PROFILE_URL')
DEMO_ACTIVITY_URL = os.environ.get('DEMO_PROFILE_URL')

st.title("Shoe Dashboard")
st.write(DEMO_PROFILE_URL)
