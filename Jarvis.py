from openai import OpenAI
import streamlit as st

st.title("gpt-4o-2024-05-13")

# Correctly accessing the API key from secrets
client = OpenAI(api_key="sk-balraj-KLoW4HxnPDr6efjrLIFlT3BlbkFJFey4fhZcJMWgg1zIqmyB")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-2024-05-13"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = ""
        for chunk in client.chat_completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            if hasattr(chunk.choices[0], 'delta') and 'content' in chunk.choices[0].delta:
                response += chunk.choices[0].delta['content']
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
