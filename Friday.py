import streamlit as st
import openai
import pandas as pd

st.set_page_config(page_title="GPT-4 Chat", page_icon=":robot_face:", layout="wide")
st.title("GPT-4 Chat Application")

# Correctly accessing the API key from secrets
api_key = st.secrets["openai_api_key"]
client = openai.OpenAI(api_key=api_key)

# Initializing session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-2024-05-13"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for model selection
st.sidebar.header("Settings")
selected_model = st.sidebar.selectbox(
    "Select Model",
    ["gpt-4o-2024-05-13", "gpt-3.5-turbo-16k-0613"],
    index=0
)
st.session_state["openai_model"] = selected_model

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Adding file uploader
st.sidebar.header("Upload Files")
uploaded_file = st.sidebar.file_uploader("Upload a file (table or screenshot)", type=["png", "jpg", "jpeg", "csv", "xlsx"])
if uploaded_file:
    if uploaded_file.type in ["image/png", "image/jpeg"]:
        st.image(uploaded_file)
    elif uploaded_file.type in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            df = pd.read_excel(uploaded_file)
        st.dataframe(df)
    st.session_state.messages.append({"role": "user", "content": f"Uploaded file: {uploaded_file.name}"})

# Chat input
prompt = st.chat_input("Ask me anything:")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.Completion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            max_tokens=300
        )

        response_text = response.choices[0].message.content
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

# Adding footer
st.sidebar.markdown("### About")
st.sidebar.info("This application is powered by OpenAI's GPT-4 model.")
