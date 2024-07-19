import openai
import streamlit as st
from PIL import Image

st.title("GPT-3.5-turbo-16k-0613 with Image Upload")

# Correctly accessing the API key from secrets
client = openai.OpenAI(api_key="sk-balraj-KLoW4HxnPDr6efjrLIFlT3BlbkFJFey4fhZcJMWgg1zIqmyB")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-16k-0613"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

uploaded_files = st.file_uploader("Upload images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name)

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        response_content = response['choices'][0]['message']['content']
        st.markdown(response_content)
    st.session_state.messages.append({"role": "assistant", "content": response_content})
