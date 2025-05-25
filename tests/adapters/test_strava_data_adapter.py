from unittest.mock import MagicMock
from adapters.strava_data_adapter import StravaDataAdapter


def test_strava_data_get_athlete():
    mock_strava = MagicMock()
    mock_strava.get_athlete.return_value = {
        "id": 1, "firstname": "Foo", "lastname": "Bar", "shoes": []}

    adapter = StravaDataAdapter(mock_strava)
    athlete = adapter.get_athlete(1)

    assert athlete['id'] == 1
    mock_strava.get_athlete.assert_called_once()


def test_strava_adapter_get_activities():
    mock_strava = MagicMock()
    mock_strava.get_activities.return_value = [
        {"id": 100, "name": "Activity 100"}]

    adapter = StravaDataAdapter(mock_strava)
    activities = adapter.get_activities(athlete_id=1, page=1, per_page=25)

    assert len(activities) == 1
    mock_strava.get_activities.assert_called_once()


def test_strava_adapter_get_activities_pages():
    mock_strava = MagicMock()
    mock_strava.get_activities.return_value = [
        {"id": 100, "name": "Activity 100"}]

    adapter = StravaDataAdapter(mock_strava)
    adapter.get_activities(athlete_id=1, page=2, per_page=25)
    assert mock_strava.get_activities.call_count == 2


def test_strava_adapter_get_gear():
    mock_strava = MagicMock()
    mock_strava.get_gear.return_value = {
        "id": "g1", "name": "ASICS Novablast 3"}

    adapter = StravaDataAdapter(mock_strava)
    shoe = adapter.get_gear("g1")

    assert shoe['name'] == 'ASICS Novablast 3'
    mock_strava.get_gear.assert_called_once()
