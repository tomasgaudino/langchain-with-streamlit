# Python libraries
import streamlit as st
import time
import os
from dotenv import load_dotenv
import pickle

import utils.utils as utils
from utils.conversation import ConversationMemory

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain

st.set_page_config(layout="wide")
load_dotenv()

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = ConversationMemory()

# Display title
st.title("LangChain")

# Sidebar configuration
st.sidebar.title("History")
previous_chats = utils.get_history_chats()

if len(previous_chats) > 0:
    chat_selected = st.sidebar.selectbox("Select previous chat", previous_chats)
    chat_selected_path = f"history/{chat_selected}"
    if st.sidebar.button("Open chat"):
        st.session_state.conversation_memory = ConversationMemory(chat_selected_path)
        chat_id = st.session_state.conversation_memory.chat_id
        st.session_state["messages"] = st.session_state.conversation_memory.session_state_messages
        st.session_state["chat_id"] = chat_id
else:
    st.sidebar.info("No previous chats found")
    chat_selected = None

st.sidebar.title("Configuration")
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.0, 0.1)

# Initialize chain with memory
llm = ChatOpenAI(temperature=temperature)
conversation = ConversationChain(
    llm=llm,
    memory=st.session_state.conversation_memory.memory,
    # verbose=True
)

utils.display_chat_history()

# Accept user input
if prompt := st.chat_input("What's up?"):
    if len(st.session_state.messages) == 0:
        st.session_state.chat_id = utils.generate_chat_id()
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = conversation.predict(input=prompt)
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Save history
    with open(f"history/{st.session_state.chat_id}.pkl", "wb") as f:
        pickle.dump(st.session_state.conversation_memory, f)


if st.sidebar.button("Clear history"):
    for chat in previous_chats:
        os.remove(f"history/{chat}")
    st.sidebar.success("History cleared")
    st.subheader("Welcome there! Do you want to start a new conversation or continue an existing one?")
    st.rerun()
