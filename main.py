import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from dotenv import load_dotenv

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


def build_activities_dataframe(activities_data, df_profile):
    df = pd.DataFrame(activities_data)

    # filter sport_type = Run
    df = df[df.sport_type == "Run"]

    # format start_date
    df['start_date_local'] = pd.to_datetime(
        df['start_date_local'])

    # convert meters to miles
    df['distance_mi'] = df['distance'] * 0.000621371

    # merge shoe dataframe
    df = pd.merge(df, df_shoes,
                  on="gear_id", how="inner")

    # filter selected shoes
    return df[['id', 'start_date_local', 'name', 'distance_mi', 'shoe_name']]


def build_shoes_dataframe(profile):
    shoes = profile['shoes']
    df = pd.DataFrame(shoes)
    df.rename(
        columns={'id': 'gear_id', 'name': 'shoe_name', 'distance': 'shoe_distance',
                 'converted_distance': 'converted_shoe_distance'},
        inplace=True)

    return df[['gear_id', 'shoe_name', 'shoe_distance', 'converted_shoe_distance']]


def build_shoe_distance_dataframe(df_activities):
    df = df_activities.copy()
    df = df.groupby(
        ['shoe_name', df['start_date_local'].dt.date])['distance_mi'].sum().reset_index()

    df_pivot = df.pivot(
        index="start_date_local",
        columns="shoe_name",
        values="distance_mi").fillna(0)
    df_pivot = df_pivot.cumsum().reset_index()
    melted = df_pivot.melt(
        id_vars=['start_date_local'], var_name='Shoe', value_name='Distance (mi)')

    return melted


def build_shoe_distance_chart(df_shoe_distance):
    fig = px.line(
        df_shoe_distance,
        x="start_date_local",
        y="Distance (mi)",
        color="Shoe",
        labels={'start_date_local': 'Date'}
    )
    fig.update_layout(
        xaxis=dict(
            tickformat="%m/%d/%Y"  # e.g., 5/1/2024
        )
    )
    return fig


profile_data = get_profile()
df_shoes = build_shoes_dataframe(profile_data)

activities_data = get_activities()
df_activities = build_activities_dataframe(activities_data, df_shoes)

df_shoe_distance = build_shoe_distance_dataframe(df_activities)
shoe_distance_fig = build_shoe_distance_chart(df_shoe_distance)
# ====  BUILD UI ==== #


def main():
    st.title("Shoe Dashboard")
    st.subheader(f"Hello {profile_data['firstname']}")

    st.subheader(f'Shoes ({len(df_shoes)})')
    st.dataframe(df_shoes.head(5))

    st.subheader(f'Activities ({len(df_activities)})')
    st.dataframe(df_activities.head(5))

    st.subheader("Stats")
    st.plotly_chart(shoe_distance_fig)


main()
