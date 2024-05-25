from openai import OpenAI
import streamlit as st

st.title("gpt-3.5-turbo-16k-0613")

# Correctly accessing the API key from secrets
client = OpenAI(api_key="sk-balraj-KLoW4HxnPDr6efjrLIFlT3BlbkFJFey4fhZcJMWgg1zIqmyB")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

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
        
        # Collect the response stream and limit to 300 characters
        response_text = ""
        for chunk in stream:
            response_text += chunk["choices"][0]["delta"]["content"]
            if len(response_text) >= 300:
                response_text = response_text[:300]
                break
        
        st.markdown(response_text)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})
