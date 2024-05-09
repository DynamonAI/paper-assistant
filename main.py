import os
import streamlit as st
from src.engine import AssistantEngine
import uuid

st.title("Seamless Pdf Assistant")
st.text("We don't save your information. All content will be reset after refresh.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    with st.chat_message("Assistant"):
        text = "Waiting for uploading pdf file."
        st.markdown(text)
        st.session_state.messages.append({"role": "Assistant", "content": text})    

with st.sidebar:
    api_key = st.text_input("OpenAI API Key", placeholder="Input your API Key")
    uploaded_file = st.file_uploader("Choose a pdf")

if api_key:
    api_key = api_key.strip()
    st.session_state.api_key_uploaded = True
    if len(st.session_state.messages) == 1:
        with st.chat_message("Assistant"):
            text = "Got your API key!"
            st.markdown(text)
            st.session_state.messages.append({"role": "Assistant", "content": text})    
    
uuid = uuid.uuid4()
file_name = f"/tmp/temp_{uuid}.pdf"
if uploaded_file is not None:
    with open(file_name, "wb") as fw:
        bytes_data = uploaded_file.getvalue()
        fw.write(bytes_data)
    if len(st.session_state.messages) == 2:
        with st.chat_message("Assistant"):
            text = "Received your file. Please wait a moment."
            st.markdown(text)
            st.session_state.messages.append({"role": "Assistant", "content": text})    

    engine = AssistantEngine(api_key, model_name="gpt-3.5-turbo", pdf_path=file_name)
    st.session_state.file_uploaded = True

if os.path.exists(file_name):
  os.remove(file_name)

if len(st.session_state.messages) == 3:
    with st.chat_message("Assistant"):
        text = "I have already read it. Please ask me questions!"
        st.markdown(text)
        st.session_state.messages.append({"role": "Assistant", "content": text})    

chat_disable = False
if "api_key_uploaded" not in st.session_state or "file_uploaded" not in st.session_state:
    chat_disable = True
prompt = st.chat_input("Ask a question", disabled=chat_disable)
if prompt:
    with st.chat_message("User"):
       st.markdown(prompt)
       st.session_state.messages.append({"role": "User", "content": prompt})
    received = engine.get_user_input(prompt)
    with st.chat_message("Assistant"):
        st.markdown(received)
        st.session_state.messages.append({"role": "Assistant", "content": received})
