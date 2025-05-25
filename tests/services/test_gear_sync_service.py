from unittest.mock import MagicMock

import pandas as pd

from adapters.strava_data_adapter import StravaDataAdapter
from services.gear_sync_service import GearSyncService


def test_gear_service_sync_sync_retired_shoes():
    mock_strava = MagicMock()
    mock_strava.get_gear.return_value = {
        'id': 'g3', 'name': "New Balance 1080v13", 'retired': True
    }
    adapter = StravaDataAdapter(mock_strava)

    mock_activity_processor = MagicMock()
    mock_activity_processor.get_missing_gear_ids.return_value = ['g3']

    mock_shoe_processor = MagicMock()
    mock_shoe_processor.get_dataframe.return_value = pd.DataFrame(
        [{"id": 1, "gear_id": "g1"}])

    service = GearSyncService(mock_activity_processor,
                              mock_shoe_processor, adapter)

    df_result = service.sync_retired_shoes()

    assert len(df_result) == 1
    mock_shoe_processor.get_dataframe.assert_called_once()
    mock_activity_processor.get_missing_gear_ids.assert_called_once()
    mock_strava.get_gear.assert_called_once()


def test_gear_service_sync_get_retired_shoes_ids():
    mock_strava = MagicMock()
    mock_strava.get_gear.return_value = {
        'id': 'g3', 'name': "New Balance 1080v13", 'retired': True
    }
    adapter = StravaDataAdapter(mock_strava)

    mock_activity_processor = MagicMock()
    mock_activity_processor.get_missing_gear_ids.return_value = ['g3']

    mock_shoe_processor = MagicMock()
    mock_shoe_processor.get_dataframe.return_value = pd.DataFrame(
        [{"id": 1, "gear_id": "g1"}])

    service = GearSyncService(mock_activity_processor,
                              mock_shoe_processor, adapter)
    result = service.get_retired_shoe_ids()

    assert len(result) == 1
    mock_activity_processor.get_missing_gear_ids.assert_called_once()
    mock_shoe_processor.get_dataframe.assert_called_once()
