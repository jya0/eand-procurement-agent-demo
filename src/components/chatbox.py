import streamlit as st


def mock_ai_response(user_input):
    return f"AI: {user_input[::-1]}"


def chatbox():
    st.title("Chat Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Create a container for messages
    messages_container = st.container()

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        ai_response = mock_ai_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Force a rerun to update the display
        st.rerun()

    # Display chat messages in the container
    with messages_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
