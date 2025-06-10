# Shoe Dashboard

Dashboard for analyzing running shoe usage and distance using Streamlit and Strava API.

Demo: [https://shoedash.streamlit.app/](https://shoedash.streamlit.app/)

## Features

- Overview Stats: number of shoes, activities, total and average mileage
- Weekly Mileage Chart: shoes used per week
- Shoe Cards: shoe total and average, mileage, activities, distance cohorts
- Charts: YOY culmulative distance, YOY weekly/monthly distance, distance cohorts
- Filter data by start/end year and shoes

## Requirements

- Python 3.12
- Streamlit
- Pandas

## Setup

1. Create .env from .env.example

2. Setup demo endpoints using [nPoint](https://www.npoint.io/) for athlete, activities, and gear data. Update .env with `DEMO_PROFILE_URL`, `DEMO_ACTIVITY_URL`, `DEMO_GEAR_URL`

   Demo Athlete:

   ```
   {
      "id": 1,
      "username": "foobar",
      "firstname": "Foo",
      "lastname": "Bar",
      "shoes": [
         {
            "id": "shoe1",
            "name": "Shoe Name",
            "distance": 1000000,
            "converted_distance": 621.0
         }
      ]
   }
   ```

   Demo Activities:

   ```
   [
      {
         "id": 1,
         "name": "Activity 1",
         "sport_type": "Run",
         "start_date_local": "2025-05-10T10:11:22Z",
         "distance": 5000,
         "gear_id": "shoe1",
      },
      {
         "id": 2,
         "name": "Activity 2",
         "sport_type": "Run",
         "start_date_local": "2025-05-11T08:17:11Z",
         "distance": 5000,
         "gear_id": "shoe2",
      }
   ]
   ```

   Demo Gear:

   ```
   [
      {
         "id": "shoe2",
         "name": "Retired Shoe",
         "retired": true,
         "distance": 684361,
         "converted_distance": 425.2,
      }
   ]
   ```

3. Create [Strava application](https://www.strava.com/settings/api) and update .env with `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`

4. Install dependencies

   `pip install -r requirements.txt`

5. Run streamlit

   `streamlit run main.py`

6. View app at `http://localhost:8501`
