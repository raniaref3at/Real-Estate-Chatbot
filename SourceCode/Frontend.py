import streamlit as st
import pandas as pd
from data_processing import load_dataset
from attribute_extraction import extract_attributes
from property_filter import search_properties
from property_formatting import format_properties

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "dataset" not in st.session_state:
    st.session_state.dataset = load_dataset()

st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 90vh;
            padding-bottom: 60px;
        }
        .chat-messages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 10px;
        }
        .user-message, .bot-message {
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 10px;
            font-size: 16px;
        }
        .user-message {
            background-color: #FFFFFF;
            color: black;
        }
        .bot-message {
            background-color: #D3D3D3;
            color: black;
        }
        .input-container {
            display: flex;
            position: fixed;
            bottom: 10px;
            left: 10px;
            right: 10px;
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        .input-box {
            flex-grow: 1;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ddd;
        }
        .send-button {
            margin-left: 10px;
            padding: 10px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

def display_chat():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

    for message in st.session_state.chat_history:
        message_type = "user-message" if message.startswith("You:") else "bot-message"
        st.markdown(f'<div class="{message_type}">{message[4:]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)



def handle_user_input():
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Enter your message:", key="user_input_field", label_visibility="collapsed")
        submit_button = st.form_submit_button("Send", type="primary")

        if submit_button and user_input:
            st.session_state.chat_history.append(f"You: {user_input}")
            
            user_attributes = extract_attributes(user_input)
            matching_properties = search_properties(user_attributes, st.session_state.dataset)
            response = format_properties(matching_properties)

            st.session_state.chat_history.append(f"Bot: {response}")
            display_chat()

handle_user_input()
