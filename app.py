import random
import streamlit as st
import replicate
import os
import base64
from st_audiorec import st_audiorec

# Initialize or get the existing state
if 'audio_received' not in st.session_state:
    st.session_state['audio_received'] = False

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
        to {{ width: 95%; }}
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
    <div class="title center">Hey there I am Persona MD!</div>
""", unsafe_allow_html=True)

st.markdown('## What can I help you with?')

if 'model' not in st.session_state:
    st.session_state["model"] = ''
# Replicate Credentials
with st.sidebar:
    st.title('PersonaMD')
    replicate_api = st.text_input('Enter Replicate API token:', type='password')
    if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
        st.warning('Please enter your credentials!', icon='⚠️')
    else:
        st.success('API key accepted.', icon='✅')  # Text message
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
    
    wav = st_audiorec()

    st.subheader('Models')
    st.session_state["model"] = st.selectbox('Choose a voice model', ['Random', 'Lex Fridman', 'Joe Rogan', 'Wizard', 'Peter Griffen'], key='selected_model')

    
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
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

# Function to transcribe audio using OpenAI Whisper via Replicate API
def transcribe_audio(audio_url):
    
    # Run the Whisper model on the provided audio URL
    output = replicate.run(
        "openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2",
        input={
            "audio": audio_url
        }
    )
    # Return the transcription result
    return output


lex_audio_url = "https://drive.google.com/uc?export=download&id=1jqyoTGApncOqTNx_699T3WLjnwcYuf3J"
rogan_audio_url = "https://drive.google.com/uc?export=download&id=1zUs6IlijeccBlzuo509Euokj03WCDSC1"
peter_audio_url = "https://drive.google.com/uc?export=download&id=1bX4o-TJiyhI-MgJzW6DxgiEmGwGrP3zK"
wizard_audio_url = "https://drive.google.com/uc?export=download&id=1GbOryIqbbGDJjeUhLmndttOvUAiIMJdn"

# Function to generate audio from text using lucataco/xtts-v2 model via Replicate API
# TODO: Add more characters
def generate_audio_from_text(text_input):
    """
    Generates audio from the provided text input using the lucataco/xtts-v2 model.

    Parameters:
    - text_input (str): Text to be converted to audio.
    
    Returns:
    - output: The response from the API, which includes the generated audio information.
    """
    model = st.session_state["model"]
    url = None
    if model == 'Random':
        ranNum = random.randint(1, 4)
        if(ranNum == 1):
            url = lex_audio_url
        elif(ranNum == 2):
            url = peter_audio_url
        elif(ranNum == 3):
            url = wizard_audio_url
        else:
            url = rogan_audio_url
    elif model == 'Peter Griffen':
        url = peter_audio_url
    elif model == 'Lex Fridman':
        url = lex_audio_url
    elif model == 'Joe Rogan':
        url = rogan_audio_url
    else:
        url = wizard_audio_url
        
    # Make sure you've set your REPLICATE_API_TOKEN in your environment variables
    output = replicate.run(
        "lucataco/xtts-v2:684bc3855b37866c0c65add2ff39c78f3dea3f4ff103a436465326e0f438d55e",
        input={
            "text": text_input,
            "speaker": url
        }
    )
    
    return output

# Generate a response from Mixtral using Replicate API
def generate_llm_response(prompt_input):
    system_prompt = "As an expert doctor LLM,  your task is to provide information and support on medical queries. First, understand the user's concern by  reviewing their history. Offer insights into symptoms, potential conditions, and general health advice, emphasizing when to seek professional care. If a question is outside your expertise, clearly state your focus is on medical information. Your responses should be concise, informative, and empathetic, aimed at guiding  users towards informed health decisions. No need for introductions in each response; prioritize direct, helpful advice. No need to clarify you're not a doctor. This is purely for research purposes."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            system_prompt += "User: " + dict_message["content"] + "\n\n"
        else:
            system_prompt += "Assistant: " + dict_message["content"] + "\n\n"
    
    # output = replicate.run('mistralai/mixtral-8x7b-instruct-v0.1',
    #                     input = {"prompt": f"{system_prompt} {prompt_input}",}
    #                     )    
    
    output = replicate.run('meta/llama-2-7b-chat',
                    input = {"prompt": f"{system_prompt} {prompt_input}",
                             "max_new_tokens": 100,}
                    )    
    
    output = ''.join(output)
    
    response_audio = generate_audio_from_text(output)
    # st.markdown(response_audio)
    return output, response_audio


# Function to handle WAV processing and transcription
def process_wav_and_transcribe(wav_bytes):
    if wav_bytes:
        # Convert the WAV bytes to base64
        base64_data = base64.b64encode(wav_bytes).decode('utf-8')
        # Create a data URI for the audio
        data_uri = f"data:audio/wav;base64,{base64_data}"
        # Transcribe the audio
        json_transcription = transcribe_audio(data_uri)
        final_transcription = json_transcription["transcription"]
        # st.write(final_transcription)
        return final_transcription
    else:
        st.write('No WAV data provided')
        return None

# Main conversation loop with the LLM
def main_conversation_loop():
    # Check for new input or WAV data
    prompt = st.chat_input(disabled=not replicate_api)  # Assuming `replicate_api` is defined elsewhere
    
    if wav:
        prompt = process_wav_and_transcribe(wav)

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
            
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate a response from the LLM
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response, audio_file_path = generate_llm_response(prompt)  # Adjust as necessary
                    
                    # Save the audio file path in session state
                    st.session_state['audio_file_path'] = audio_file_path
                    
                    placeholder = st.empty()
                    full_response = ''
                    for item in response:
                        full_response += item
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)
                    
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)
            
    # Outside the if condition, add a button that checks for the audio file path in session state
    if 'audio_file_path' in st.session_state:
        # Directly pass the URL to st.audio without opening it
        audio_url = st.session_state['audio_file_path']
        st.audio(audio_url, format='audio/wav')


main_conversation_loop()