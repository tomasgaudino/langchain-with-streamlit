import os
import uuid
import streamlit as st

from langchain.schema import HumanMessage

HISTORY_PATH = "history"


def get_history_chats():
    """Get history chats from history folder"""
    return [file for file in os.listdir(HISTORY_PATH) if file.endswith(".pkl")]


def generate_chat_id():
    """Generate a unique id for a history chat"""
    history_chats_ids = get_history_chats()
    new_id = str(uuid.uuid4())[:8]
    while new_id in history_chats_ids:
        new_id = str(uuid.uuid4())[:8]
    return new_id


def display_chat_history():
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
