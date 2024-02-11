# Project for Hacklytics 2024!

Welcome to Persona MD! A service that takes the stress off searching for obscure answers to your at home medical questions in a fun, easy, and accessible way!

## Table of Contents
1. [Technologies](#technologies)
2. [Setup Instructions](#setup-instructions)
3. [Features](#features)

## Technologies
- Streamlit
- Replicate
- Whisper
- XTTS-2
- Mixtral
- Digital Ocean

## Setup Instructions
  ```
  conda create -n digistream python=3.10 -y
  conda activate digistream
  ```
  
  Install requirements file
  
  ```
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

## Features
- **Text and Audio Input**: Users can input their medical concerns using either text or audio, making it convenient for individuals with different communication preferences.
- **Simulated Medical LLM**: The project utilizes a powerful open source large language model to understand and interpret the user's input, providing accurate and reliable recommendations.
- **Text-to-Speech with Audio Cloning**: Persona MD offers text-to-speech functionality, along with audio cloning, to alleviate the stress and anxiety associated with medical complications. This feature ensures that the information is accessible to a wider audience, including those with visual impairments.
