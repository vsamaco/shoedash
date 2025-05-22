from repositories.activity_repository import ActivityRepository


activities_data = [
    {
        "id": 1,
        "sport_type": "Run",
        "start_date": "2024-12-15T23:01:20Z",
        "start_date_local": "2024-12-15T15:01:20Z",
        "name": "Run 1",
        "distance": 5000,
        "moving_time": 6702,
        "gear_id": "g1",
    }
]


def test_get_activities_df():
    repo = ActivityRepository(activities_data)
    df_activities = repo.get_activities_df()
    assert len(df_activities) == 1
    assert round(df_activities.iloc[0]['distance_mi'], 2) == 3.11
