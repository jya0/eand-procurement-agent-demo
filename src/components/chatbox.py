import streamlit as st


def mock_ai_response(user_input):
    return f"AI: {user_input[::-1]}"


def chatbox():
    st.header("Chat Assistant")
    
    # Initialize messages if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Create a scrollable area for messages
    messages_html = ""
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if role == "user":
            messages_html += f'<div style="text-align: right; margin: 5px;"><b>You:</b> {content}</div>'
        else:
            messages_html += f'<div style="text-align: left; margin: 5px;"><b>Assistant:</b> {content}</div>'
    
    # Render messages in a fixed-height scrollable div
    st.markdown(
        f"""
        <div style="height: 800px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">
            {messages_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Chat input remains fixed below the scrollable area
    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        ai_response = mock_ai_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        st.rerun()