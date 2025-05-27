from unittest.mock import MagicMock, patch
from streamlit.testing.v1 import AppTest

from adapters.demo_data_adapter import DemoDataAdapter

test_athlete = {
    "id": 1,
    "username": "foobar",
    "firstname": "Foo",
    "lastname": "Bar",
    "shoes": [{
        "id": "g1",
        "name": "ASICS Novablast 3",
        "converted_distance": 648.6,
        "retired": False,
    }]
}

test_retired_gear = {
    "id": "g3",
    "name": "Retired Shoe",
    "retired": True,
    "converted_distance": 100.0,
}

test_activities = [
    {
        "id": 100,
        "sport_type": "Run",
        "name": "Test Run 1",
        "distance": 5000,
        "start_date": "2025-01-04T16:36:59Z",
        "start_date_local": "2025-01-04T08:36:59Z",
        "gear_id": "g1",
    },
    {
        "id": 100,
        "sport_type": "Run",
        "name": "Test Run 2",
        "distance": 5000,
        "start_date": "2025-01-12T22:16:41Z",
        "start_date_local": "2025-01-12T14:16:41Z",
        "gear_id": "g1",
    },
    {
        "id": 100,
        "sport_type": "Run",
        "name": "Test Run 3",
        "distance": 5000,
        "start_date": "2025-01-12T22:16:41Z",
        "start_date_local": "2025-01-12T14:16:41Z",
        "gear_id": "g3",
    }
]


def test_demo():
    with patch.object(DemoDataAdapter, 'get_athlete', return_value=test_athlete), \
            patch.object(DemoDataAdapter, 'get_activities', return_value=test_activities), \
            patch.object(DemoDataAdapter, 'get_gear', return_value=test_retired_gear):
        at = AppTest.from_file('main.py').run()

        # Sidebar State
        assert at.sidebar.selectbox(key="selected_mode").value == "demo"
        assert at.sidebar.checkbox(key="check_retired_shoes").value is False
        assert at.sidebar.checkbox(
            key="check_retired_shoes").label == "Include Retired Shoes: 1"
        assert at.sidebar.selectbox(key="activity_start_year").value == 2025
        assert at.sidebar.selectbox(key="activity_end_year").value == 2025
        assert not at.sidebar.multiselect(key="selected_shoes").value

        # Main State
        assert at.main.subheader[0].value == "Hello Foo"

        # Main Overview
        assert at.main.text[0].value == "1/04/2025 - 1/12/2025"
        assert at.main.metric[0].value == "1"  # Num Shoes
        assert at.main.metric[1].value == "9 mi"  # Total Activity Mileage
        assert at.main.metric[2].value == "3"  # Num Activities
        assert at.main.metric[3].value == "5 mi"  # Weekly Mileage

        # Main Shoe Card
        assert at.subheader[4].value == "ASICS Novablast 3"
        assert at.metric[4].value == "649 mi"  # Shoe Total Miles
        assert at.metric[5].value == "2"  # Shoe Num Activities
        assert at.metric[6].value == "3.1 mi"  # Shoe Average Miles
