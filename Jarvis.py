from openai import OpenAI
import streamlit as st
import requests

st.title("gpt-3.5-turbo-16k-0613")

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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Adding file uploader
uploaded_file = st.file_uploader("Upload a file (table or screenshot)", type=["png", "jpg", "jpeg", "csv", "xlsx"])
if uploaded_file:
    if uploaded_file.type in ["image/png", "image/jpeg"]:
        st.image(uploaded_file)
    elif uploaded_file.type in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        st.write(f"File uploaded: {uploaded_file.name}")
        if uploaded_file.type == "text/csv":
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            st.dataframe(df)
    st.session_state.messages.append({"role": "user", "content": f"Uploaded file: {uploaded_file.name}"})

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
