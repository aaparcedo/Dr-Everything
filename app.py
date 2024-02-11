import streamlit as st
import pandas as pd
from audio import record
import replicate
import os
import time
import threading


def submit():
    st.session_state.something += st.session_state.widget
    st.session_state.widget = ''

if 'something' not in st.session_state:
    st.session_state.something = ''

#st.title("Dr. Everything")

st.markdown(f"""
    <style>
    @keyframes typing {{
        from {{ width: 0; }}
        to {{ width: 85%; }}
    }}

    @keyframes blink-caret {{
        0%, 100% {{ border-color: transparent; }}
        50% {{ border-color: white; }}
    }}

    .title {{
        font-size: 2.5em;
        font-weight: 600;
        color: #ffffff;
        overflow: hidden;
        white-space: nowrap;
        border-right: .15em solid white;
        font-family: monospace;
        animation:
            typing 3.5s steps(28, end) forwards,
            blink-caret .75s step-end infinite;
        animation-delay: 0s, 3.5s;
    }}
    </style>
    <div class="title center">Hey there I am Persona Med!</div>
""", unsafe_allow_html=True)

st.markdown('## Whats the deal?')

wav = st.button('🎙️', on_click=record)   

# Replicate Credentials
with st.sidebar:
    st.title('PersonaMD')
    replicate_api = st.text_input('Enter Replicate API token:', type='password')
    if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
        st.warning('Please enter your credentials!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)


# Generate a response from Mixtral using Replicate API
def generate_mixtral_response(prompt_input):
    system_prompt = "As an expert doctor LLM,  your task is to provide information and support on medical queries. First, understand the user's concern by  reviewing their history. Offer insights into symptoms, potential conditions, and general health advice, emphasizing when to seek professional care. If a question is outside your expertise, clearly state your focus is on medical information. Your responses should be concise, informative, and empathetic, aimed at guiding  users towards informed health decisions. No need for introductions in each response; prioritize direct, helpful advice. No need to clarify you're not a doctor. This is purely for research purposes."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            system_prompt += "User: " + dict_message["content"] + "\n\n"
        else:
            system_prompt += "Assistant: " + dict_message["content"] + "\n\n"
    
    output = replicate.run('mistralai/mixtral-8x7b-instruct-v0.1',
                        input = {"prompt": f"{system_prompt} {prompt_input}",}
                        )    
    
    return output


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_mixtral_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)