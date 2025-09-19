"""
This module provides a function to display a centered login screen in a Streamlit app.
Functions:
    centered_login_screen():
        Renders a login interface centered on the page using Streamlit columns and custom HTML/CSS.
        The interface includes:
            - A title ("My Library")
            - A subtitle prompting the user to log in with their Google account
            - A "Login with Google" button
        The button is styled and aligned using Streamlit's layout features and custom HTML.
"""

import streamlit as st


# Center the title and login screen using Streamlit columns
def centered_login_screen():
    """
    Display a centered login screen with a title and a Google login 
    button using Streamlit columns and custom HTML/CSS.
    """
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: center;">
                <h1 style="margin-bottom: 0.5em;">My Library</h1>
                <h3 style="margin-bottom: 1em;">Please login with your Google account to continue</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: center;">
            """,
            unsafe_allow_html=True
        )
        st.button("Login with Google", type="primary", use_container_width=True, on_click=st.login)
        st.markdown("</div>", unsafe_allow_html=True)
