import streamlit as st
import pandas as pd
from audio import record


def submit():
    st.session_state.something += st.session_state.widget
    st.session_state.widget = ''

if 'something' not in st.session_state:
    st.session_state.something = ''

st.title("Dr. Everything at ya service...")

st.markdown('## Whats the deal?')

st.button('🎙️', on_click=record)   
st.text_input('Enter text...', key='widget', on_change=submit)

st.write(f'Last submission: {st.session_state.something}')
