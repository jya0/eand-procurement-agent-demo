import streamlit as st
from typing import Dict, List


def mock_ai_response(user_input: str) -> str:
    """
    Generate a mock AI response by reversing the input string.
    
    Args:
        user_input (str): The user's input message
        
    Returns:
        str: The AI's response
    """
    return f"AI: {user_input[::-1]}"


def chatbox() -> None:
    """
    Display and manage the chat interface.
    Handles message history, user input, and AI responses.
    """
    # Set up the chat interface
    st.title("Chat Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    messages_container = st.container()

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        ai_response = mock_ai_response(prompt)
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })
        
        st.rerun()

    with messages_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
