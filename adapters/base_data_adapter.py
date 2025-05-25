from abc import ABC, abstractmethod
import streamlit as st


class BaseDataAdapter(ABC):
    @abstractmethod
    def get_mode(self):
        pass

    @abstractmethod
    def get_athlete(self, athlete_id):
        pass

    @abstractmethod
    def get_activities(self, athlete_id, per_page, page):
        pass

    @abstractmethod
    def get_gear(self, gear_id):
        pass


@st.cache_data
def get_athlete(_adapter: BaseDataAdapter, mode, athlete_id):
    return _adapter.get_athlete(athlete_id)


@st.cache_data
def get_activities(_adapter: BaseDataAdapter, mode, athlete_id, page=1, per_page=100):
    print(f'get activities mode:{mode} page: {page}')
    return _adapter.get_activities(athlete_id=athlete_id, page=page, per_page=per_page)


@st.cache_data
def get_gear(_adapter: BaseDataAdapter, mode, gear_id):
    return _adapter.get_gear(gear_id)
