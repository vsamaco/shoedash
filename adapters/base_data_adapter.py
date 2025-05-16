from abc import ABC, abstractmethod
import streamlit as st


class BaseDataAdapter(ABC):
    @abstractmethod
    def get_athlete(self, athlete_id):
        pass

    @abstractmethod
    def get_activities(self, athlete_id, per_page, page):
        pass


@st.cache_data
def get_athlete(_adapter: BaseDataAdapter, mode, athlete_id):
    return _adapter.get_athlete(athlete_id)


@st.cache_data
def get_activities(_adapter: BaseDataAdapter, mode, athlete_id, page=1, per_page=100):
    return _adapter.get_activities(athlete_id=athlete_id, page=page, per_page=per_page)
