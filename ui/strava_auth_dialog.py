import streamlit as st


class StravaAuthDialog():
    def __init__(self, login_url, cancel_action):
        self.login_url = login_url
        self.cancel_action = cancel_action

    @st.dialog("Change Source", width='small')
    def render(self):
        st.markdown("""
            <style>
                div[data-testid="stColumn"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="stColumn"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"[![Connect with Strava](app/static/images/btn_strava_connect_with_orange.png)]({self.login_url})")
        with col2:
            if st.button('Cancel'):
                self.cancel_action()
        st.stop()
