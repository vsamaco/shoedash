from abc import ABC, abstractmethod
import streamlit as st


class BaseDataAdapter(ABC):
    @abstractmethod
    def get_athlete(self, athlete_id):
        pass

    @abstractmethod
    def get_activities(self, athlete_id):
        pass


@st.cache_data
def get_athlete(_adapter: BaseDataAdapter, athlete_id):
    return _adapter.get_athlete(athlete_id)


@st.cache_data
def get_activities(_adapter, athlete_id):
    return _adapter.get_activities(athlete_id)
