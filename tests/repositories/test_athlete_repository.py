from unittest.mock import MagicMock, patch
from repositories.athlete_repository import AthleteRepository


athlete_data = {
    "id": 1,
    "firstname": "Foo",
    "lastname": "Bar",
    "shoes": [
        {"id": "g1", "name": "Saucony Ride 15",
            "converted_distance": 100, "retired": "false"},
        {"id": "g2", "name": "ASICS Novablast 4",
            "converted_distance": 50, "retired": "false"},
    ]
}


@patch('repositories.athlete_repository.ShoeProcessor')
def test_get_profile(_mock_shoe_processor_class):
    repo = AthleteRepository(athlete_data)
    assert repo.get_profile() == athlete_data


@patch('repositories.athlete_repository.ShoeProcessor')
def test_get_shoes_names(mock_shoe_processor_class):
    mock_shoe_processor = MagicMock()
    mock_shoe_processor.get_shoe_name_list.return_value = ['Saucony', 'ASICS']
    mock_shoe_processor_class.return_value = mock_shoe_processor

    repo = AthleteRepository(athlete_data)
    result = repo.get_shoes_names()

    assert result == ['Saucony', 'ASICS']
    mock_shoe_processor.get_shoe_name_list.assert_called_once()


@patch('repositories.athlete_repository.ShoeProcessor')
def test_get_shoes_df(mock_shoe_processor_class):
    mock_shoe_processor = MagicMock()
    mock_filtered = MagicMock()
    mock_filtered.get_dataframe.return_value = "mocked"
    mock_shoe_processor.filter_shoes_by_name.return_value = mock_filtered
    mock_shoe_processor_class.return_value = mock_shoe_processor

    repo = AthleteRepository(athlete_data)
    repo.get_shoes_df()
    mock_shoe_processor.filter_shoes_by_name.assert_called_once()
    mock_filtered.get_dataframe.assert_called_once()
