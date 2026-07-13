"""
language_selector.py

Komponente zur Auswahl der Sprache
für die Weather App.
"""

import streamlit as st

from frontend.config import (
    LANGUAGES,
    DEFAULT_LANGUAGE
)


def init_language():
    """
    Initialisiert die Sprache im Session-State.
    """

    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE



def set_language(language_code):
    """
    Speichert die ausgewählte Sprache.

    Args:
        language_code (str):
            Sprachcode z.B. de, en, fr
    """

    st.session_state.language = language_code



def render_language_selector():
    """
    Rendert die Sprachbuttons im Header.

    Returns:
        str:
            Aktuell ausgewählte Sprache.
    """

    init_language()


    columns = st.columns(
        len(LANGUAGES),
        gap="small"
    )


    for column, (flag, data) in zip(
        columns,
        LANGUAGES.items()
    ):

        with column:

            active = (
                st.session_state.language
                ==
                data["code"]
            )


            button_label = flag


            if active:

                button_label = (
                    f"🔴 {flag}"
                )


            if st.button(
                button_label,
                key=f"language_{data['code']}",
                use_container_width=True
            ):

                set_language(
                    data["code"]
                )

                st.rerun()


    return st.session_state.language