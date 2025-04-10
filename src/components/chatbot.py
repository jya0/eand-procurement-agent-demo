import streamlit as st
import os
from cerebras.cloud.sdk import Cerebras


def update_chatbot_context(cerebrasClient, context):
    try:
        chat_completion = cerebrasClient.chat.completions.create(
            model=model_option,
            messages=[{"role": "user", "content": context}],
        )

        # Display response from Cerebras API
        # with st.chat_message("assistant", avatar="🤖"):
        response = chat_completion.choices[0].message.content
        # Save response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        # st.markdown(response)
    except Exception as e:
        st.error(e, icon="🚨")


def display_intro():
    # Header with icon and title
    col1, col2 = st.columns([1, 5])

    with col1:
        # Robot emoji as the chatbot icon
        st.write("# 🤖")

    with col2:
        st.title("Supplier Assistant")

    # Main description with icons
    st.write(
        """
    ### ✨ Chat with an assistant and effortlessly re-rank the most relevant suppliers. 
    """
    )

    st.divider()

    st.subheader("Key Functionalities", divider=True)

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:
        st.write("🔍 **Smart Filter**")
        st.write("Filter suppliers based on your prompts in seconds")

        st.write("🔄 **Re-ranking**")
        st.write("Rank suppliers relevant to your criteria in Gold, Silver and Bronze")

    with feature_col2:
        st.write("💬 **Natural Conversations**")
        st.write("Ask questions in plain language and get intelligent responses")

        st.write("📊 **Data-Driven Insights**")
        st.write("Make decisions based on supplier performance metrics")

    # st.subheader("How It Works", divider=True)

    # steps_col1, steps_col2, steps_col3 = st.columns(3)

    # with steps_col1:
    #     st.write("1️⃣ **Ask a Question**")
    #     st.write("Describe what you're looking for in simple terms")

    # with steps_col2:
    #     st.write("2️⃣ **Review Results**")
    #     st.write("See a ranked list of matching suppliers")

    # with steps_col3:
    #     st.write("3️⃣ **Refine & Explore**")
    #     st.write("Ask follow-up questions to get exactly what you need")

    # with st.expander("💡 Tips for best results"):
    #     st.write(
    #         """
    #     - Be specific about your requirements
    #     - Include information about quantity, price, and delivery time
    #     - Ask for comparisons between different suppliers
    #     - Request specific data points about supplier performance
    #     """
    #     )
    # st.divider()

    # cta_col1, cta_col2 = st.columns([3, 1])

    # with cta_col1:
    #     st.write("### Ready to find your perfect supplier match?")

    # with cta_col2:
    #     start_button = st.button("Start Chat", use_container_width=True)


def show_chatbot():
    with st.container():
        with st.columns([1, 11, 1])[1]:
            textArea = st.container(border=True, height=450)
            with textArea:
                display_intro()
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
                "llama3.1-8b": {
                    "name": "Llama3.1-8b",
                    "tokens": 8192,
                    "developer": "Meta",
                },
                "llama-3.3-70b": {
                    "name": "Llama-3.3-70b",
                    "tokens": 8192,
                    "developer": "Meta",
                },
            }

            # Layout for model selection and max_tokens slider
            # col1, col2 = st.columns(2)

            # with col1:
            #     model_option = st.selectbox(
            #         "Choose a model:",
            #         options=list(models.keys()),
            #         format_func=lambda x: models[x]["name"],
            #     )

            # Detect model change and clear chat history if model has changed
            # if st.session_state.selected_model != model_option:
            #     st.session_state.messages = []
            #     st.session_state.selected_model = model_option

            # max_tokens_range = models[model_option]["tokens"]

            # with col2:
            #     # Adjust max_tokens slider based on the selected model
            #     max_tokens = st.slider(
            #         "Max Tokens:",
            #         min_value=512,
            #         max_value=max_tokens_range,
            #         value=max_tokens_range,
            #         step=512,
            #         help=f"Select the maximum number of tokens (words) for the model's response.",
            #     )

            # st.write(st.session_state)
            # Display chat messages stored in history on app rerun
            model_option = "llama-3.3-70b"

            with textArea:
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
                    )

                    # Display response from Cerebras API
                    # with st.chat_message("assistant", avatar="🤖"):
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
