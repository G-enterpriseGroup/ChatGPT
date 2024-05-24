import json
from openai import OpenAI
import streamlit as st
import requests
import pandas as pd
from gtts import gTTS
import os

st.title("Enhanced GPT-3.5-turbo-16k-0613 Chat")

# Correctly accessing the API key from secrets
api_key = "sk-balraj-KLoW4HxnPDr6efjrLIFlT3BlbkFJFey4fhZcJMWgg1zIqmyB"
client = OpenAI(api_key=api_key)

def get_api_limits(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get("https://api.openai.com/v1/usage", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('daily_limit', 'Unknown'), data.get('remaining', 'Unknown')
    else:
        return 'Unknown', 'Unknown'

daily_limit, remaining_limit = get_api_limits(api_key)
st.sidebar.write(f"Daily Limit: {daily_limit}")
st.sidebar.write(f"Remaining Limit: {remaining_limit}")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-16k-0613"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Export/Import chat history
def export_history():
    with open("chat_history.json", "w") as f:
        json.dump(st.session_state.messages, f)

def import_history():
    with open("chat_history.json", "r") as f:
        st.session_state.messages = json.load(f)

if st.sidebar.button("Export Chat History"):
    export_history()
    st.sidebar.success("Chat history exported.")

if st.sidebar.button("Import Chat History"):
    import_history()
    st.sidebar.success("Chat history imported.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Adding file uploader
uploaded_file = st.file_uploader("Upload a file (table or screenshot)", type=["png", "jpg", "jpeg", "csv", "xlsx", "pdf"])
if uploaded_file:
    if uploaded_file.type in ["image/png", "image/jpeg"]:
        st.image(uploaded_file)
    elif uploaded_file.type in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        st.write(f"File uploaded: {uploaded_file.name}")
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            st.dataframe(df)
    elif uploaded_file.type == "application/pdf":
        st.write(f"File uploaded: {uploaded_file.name}")
        # Add PDF processing here
    st.session_state.messages.append({"role": "user", "content": f"Uploaded file: {uploaded_file.name}"})

# Language translation (example)
def translate_text(text, target_lang="es"):
    response = requests.post(
        "https://api.openai.com/v1/translations",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"text": text, "target_lang": target_lang}
    )
    if response.status_code == 200:
        return response.json()["translation"]
    else:
        return text

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Voice input/output (example)
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    return "response.mp3"

if st.sidebar.button("Play Response as Speech"):
    if st.session_state.messages:
        last_message = st.session_state.messages[-1]["content"]
        audio_file = text_to_speech(last_message)
        st.audio(audio_file)
        os.remove(audio_file)
