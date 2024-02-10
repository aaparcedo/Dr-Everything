import streamlit as st
import pandas as pd
from audio import record

st.title("Dr. Everything at ya service...")

st.markdown('## Whats the deal?')

if 'something' not in st.session_state:
    st.session_state.something = ''

def submit():
    st.session_state.something = st.session_state.widget
    st.session_state.widget = ''

st.text_input('Enter text...', key='widget', on_change=submit)

st.write(f'Last submission: {st.session_state.something}')

st.button('record audio', on_click=record)