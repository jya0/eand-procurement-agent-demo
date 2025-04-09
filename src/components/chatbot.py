import streamlit as st
import os
from cerebras.cloud.sdk import Cerebras


st.title("Cerebras")
st.subheader("Deploying Cerebras on Streamlit", divider="orange", anchor=False)

def show_chatbot() -> None:
    with st.container(border=True):
        api_key = os.getenv("CEREBRAS_API_KEY")
        if not api_key:
            st.warning("API KEY MISSING!")
            st.stop()

        # Create the Cerebras client
        client = Cerebras(
            # This is the default and can be omitted
            api_key=api_key,
        )

        # Initialize chat history and selected model
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "selected_model" not in st.session_state:
            st.session_state.selected_model = None

        # Define model details
        models = {
            "llama3.1-8b": {"name": "Llama3.1-8b", "tokens": 8192, "developer": "Meta"},
            "llama-3.3-70b": {"name": "Llama-3.3-70b", "tokens": 8192, "developer": "Meta"},
        }

        # Layout for model selection and max_tokens slider
        col1, col2 = st.columns(2)

        with col1:
            model_option = st.selectbox(
                "Choose a model:",
                options=list(models.keys()),
                format_func=lambda x: models[x]["name"],
            )

        # Detect model change and clear chat history if model has changed
        if st.session_state.selected_model != model_option:
            st.session_state.messages = []
            st.session_state.selected_model = model_option

        max_tokens_range = models[model_option]["tokens"]

        with col2:
            # Adjust max_tokens slider based on the selected model
            max_tokens = st.slider(
                "Max Tokens:",
                min_value=512,
                max_value=max_tokens_range,
                value=max_tokens_range,
                step=512,
                help=f"Select the maximum number of tokens (words) for the model's response.",
            )

        # st.write(st.session_state)
        # Display chat messages stored in history on app rerun

        for message in st.session_state.messages:
            avatar = "🤖" if message["role"] == "assistant" else "🦔"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
        if prompt := st.chat_input("Enter your prompt here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            try:
                chat_completion = client.chat.completions.create(
                    model=model_option,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                )

                # Display response from Cerebras API
                with st.chat_message("assistant", avatar="🤖"):
                    response = chat_completion.choices[0].message.content
                    # Save response to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                    # st.markdown(response)
            except Exception as e:
                st.error(e, icon="🚨")
            st.rerun()


# st.title("Echo Bot")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun


# Function to process user input
# def process_input(user_input):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     # Generate response
#     response = f"Echo: {user_input}"
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})


# with st.container():
#     # Get user input
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
#     if prompt := st.chat_input("What is up?"):
#         process_input(prompt)
#         # Rerun the app to display the new messages
#         st.rerun()

# st.write("Outside container")
