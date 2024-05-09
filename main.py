import os
import streamlit as st
from src.engine import AssistantEngine
import uuid

st.title("Seamless Pdf Assistant")
st.text("We don't save your information. All content will be reset after refresh.")

def init():
    st.session_state.api_input_visble = True
    st.session_state.uploader_input_visible = True
    st.session_state.chat_input_disable = True

if "messages" not in st.session_state:
    st.session_state.messages = []
    init()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def api_input_callback():
    st.session_state.api_key = st.session_state.api_key.strip()
    st.session_state.api_input_visble = False
    st.toast("Got your API Key!")
    
api_key = None
if st.session_state.api_input_visble:
    with st.sidebar:
        api_key = st.text_input(
            "1. OpenAI API Key",
            placeholder="Input your API Key,",
            key="api_key",
            on_change=api_input_callback)

if "api_key" in st.session_state:
    engine = st.session_state.api_key
    
def file_callback():
    st.session_state.uploader_input_visible = False
    uid = uuid.uuid4()
    file_name = f"/tmp/temp_{uid}.pdf"
    with open(file_name, "wb") as fw:
        bytes_data = st.session_state.uploaded_file.getvalue()
        fw.write(bytes_data)
    st.toast("Received your file. Please wait a moment.")
    engine = AssistantEngine(api_key, model_name="gpt-3.5-turbo", pdf_path=file_name)
    st.session_state.engine = engine
    st.toast("Come on! Ask me a question!")
    st.balloons()
    st.session_state.chat_input_disable = False
    
    if os.path.exists(file_name):
      os.remove(file_name)

engine = None
if st.session_state.uploader_input_visible:
    with st.sidebar:
        uploaded_file = st.file_uploader(
            "2. Choose a pdf",
            key="uploaded_file",
            on_change=file_callback
        )


if "engine" in st.session_state:
    engine = st.session_state.engine


prompt = st.chat_input("Ask a question", disabled=st.session_state.chat_input_disable)
if prompt:
    with st.chat_message("User"):
       st.markdown(prompt)
       st.session_state.messages.append({"role": "User", "content": prompt})
    received = engine.get_user_input(prompt)
    with st.chat_message("Assistant"):
        st.markdown(received)
        st.session_state.messages.append({"role": "Assistant", "content": received})
