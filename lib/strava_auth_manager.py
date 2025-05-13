import streamlit as st
from lib.strava import Strava


class StravaAuthManager():
    def __init__(self, strava: Strava):
        self.strava = strava

    def handle_auth(self, mode):
        code = st.query_params.get('code')
        # validate code, when code
        if code:
            self.validate_code(code)
        # login when mode=strava, code=None, strava.access_token=None
        elif mode == 'strava' and not code and not self.strava.access_token:
            self.render_login()
        # no op, when mode=demo

    def render_login(self):
        st.markdown(
            f'<a href="{self.strava.get_login_url()}" target="_self">Login Strava</a>', unsafe_allow_html=True)
        st.stop()

    def validate_code(self, code):
        if self.strava.request_access_token(code):
            st.session_state.mode = 'strava'
            st.query_params.clear()
        else:
            st.error('auth error')
            self.render_login()
