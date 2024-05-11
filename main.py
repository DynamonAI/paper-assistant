import os
import streamlit as st
from src.engine import AssistantEngine
import logging
import uuid

avatars = {
    "User": None,
    "Assistant": None
}

with st.sidebar:
    st.title('Paper Assistant')
    st.markdown('We do not save your data. All content and information will be cleaned after refresh.')

def init():
    st.session_state.api_input_visble = True
    st.session_state.uploader_input_visible = True
    st.session_state.chat_input_disable = True

if "messages" not in st.session_state:
    st.session_state.messages = []
    init()

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatars[message["role"]]):
        st.markdown(message["content"])

def api_input_callback():
    st.session_state.api_key = st.session_state.api_key_input.strip()
    st.session_state.api_input_visble = False
    st.toast("Got your API Key!")
    
api_key = None
if st.session_state.api_input_visble:
    with st.sidebar:
        st.text_input(
            "OpenAI API Key",
            placeholder="Input your API Key",
            key="api_key_input",
            on_change=api_input_callback)

if "api_key" in st.session_state and len(st.session_state.api_key) > 0:
    api_key = st.session_state.api_key
    with st.sidebar:
        st.success('API key already provided!', icon='✅')
    
def file_callback():
    st.session_state.uploader_input_visible = False
    uid = uuid.uuid4()
    file_name = f"/tmp/temp_{uid}.pdf"
    with open(file_name, "wb") as fw:
        bytes_data = st.session_state.uploaded_file.getvalue()
        fw.write(bytes_data)
    st.toast("Received your file. Please wait a moment.")
    with st.spinner('I am processing the paper uploaded. It might take a few minutes...'):
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
        st.file_uploader(
            "Choose a Paper",
            key="uploaded_file",
            on_change=file_callback,
            type="pdf"
        )


if "engine" in st.session_state:
    engine = st.session_state.engine
    with st.sidebar:
        st.success('File already uploaded!', icon='✅')


def stream_wrapper(prompt,respone):
    def get_stream_rep():
        collected_messages = []
        for chunk in respone:
            chunk_message = chunk.choices[0].delta.content
            if chunk_message is None:
                continue
#             collected_messages.append(chunk_message)
            yield chunk_message
#         collected_messages = "".join([m for m in collected_messages if m is not None])
#         st.session_state.collected_messages = collected_messages
#         st.session_state.messages.append({"role": "Assistant", "content": collected_messages})
#         engine.interface.append_message("assistant", collected_messages)
    return get_stream_rep

with st.sidebar:
    st.markdown('<p>Powered by <a href="https://DynamonAI.com">DynamonAI</a></p>', unsafe_allow_html=True)


def chat_input_callback():
    pass

if prompt := st.chat_input(
    "Ask a question",
    disabled=st.session_state.chat_input_disable,
    on_submit=chat_input_callback,
    key="prompt"
):
    prompt = st.session_state.prompt
    with st.chat_message("User", avatar=avatars["User"]):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "User", "content": prompt})
    received = engine.get_completion(prompt, return_text=False, stream=True)
    stream_func = stream_wrapper(prompt, received)
    with st.chat_message("Assistant", avatar=avatars["Assistant"]):
        full_response =  st.write_stream(stream_func)
#         placeholder = st.empty()
#         full_response = ''
#         stream_obj = stream_func()
#         for item in stream_obj:
#             full_response += item
#             placeholder.markdown(full_response)
#         placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "Assistant", "content": full_response})
        engine.interface.append_message("assistant", full_response)

