import streamlit as st
from lib.strava import Strava
from ui.strava_auth_dialog import StravaAuthDialog


class StravaAuthManager():
    def __init__(self, strava: Strava):
        self.strava = strava

    def handle_auth(self, mode):
        code = st.query_params.get('code')
        # validate code after strava auth confirmed
        if code:
            self.validate_code(code)
        # prompt strava login
        elif mode == 'strava' and not code and not self.strava.access_token:
            self._display_auth_dialog()

    def validate_code(self, code):
        if self.strava.request_access_token(code):
            st.session_state.mode = 'strava'
            st.query_params.clear()
        else:
            st.error('auth error')
            self._display_auth_dialog()

    def _display_auth_dialog(self):
        def cancel_action():
            st.session_state.mode = 'demo'
            st.session_state.selected_mode = 'demo'
            st.rerun()
        StravaAuthDialog(self.strava.get_login_url(), cancel_action).render()
