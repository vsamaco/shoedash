from unittest.mock import MagicMock, patch
from adapters.demo_data_adapter import DemoDataAdapter


@patch('adapters.demo_data_adapter.requests.get')
def test_demo_adapter_get_athlete(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": 1, "firstname": "Foo", "lastname": "Bar", "shoes": []}
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    adapter = DemoDataAdapter()
    athlete = adapter.get_athlete(1)

    assert athlete['id'] == 1
    mock_get.assert_called_once()


@patch('adapters.demo_data_adapter.requests.get')
def test_demo_adapter_get_activities(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [{
        "id": 100, "name": "Activity 100"}]
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    adapter = DemoDataAdapter()
    activities = adapter.get_activities(1)

    assert len(activities) == 1
    mock_get.assert_called_once()


@patch('adapters.demo_data_adapter.requests.get')
def test_demo_adapter_get_gear(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "g1", "name": "ASICS Novablast 3", "retired": True}
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    adapter = DemoDataAdapter()
    shoe = adapter.get_gear("g1")

    assert shoe['name'] == "ASICS Novablast 3"
    mock_get.assert_called_once()
