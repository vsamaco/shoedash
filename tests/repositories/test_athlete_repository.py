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


def test_get_profile():
    repo = AthleteRepository(athlete_data)
    assert repo.get_profile() == athlete_data


def test_get_shoes_df():
    repo = AthleteRepository(athlete_data)
    df_shoes = repo.get_shoes_df()

    assert len(df_shoes) == 2
    assert df_shoes['name'].to_list() == ['Saucony Ride 15',
                                          'ASICS Novablast 4']
