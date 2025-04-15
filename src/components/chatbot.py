import streamlit as st
import os
from cerebras.cloud.sdk import Cerebras
from streamlit_extras.stylable_container import stylable_container


def display_intro():
    st.header("✨ Chat with an assistant and effortlessly re-rank the most relevant suppliers.", anchor=False)

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


class ChatbotClient:
    """
    A class to handle interactions with the Cerebras API for chatbot functionality.
    """

    def __init__(self, api_key=None):
        """
        Initialize the ChatbotClient with API key and models information.

        Args:
            api_key: The Cerebras API key. If None, tries to get from environment variables.
        """
        self.api_key = api_key or os.getenv("CEREBRAS_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required to initialize ChatbotClient")

        self.client = Cerebras(api_key=self.api_key)

        # Define available models and their details
        self.models = {
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

        # Default model
        self.default_model = "llama-3.3-70b"

    def get_available_models(self):
        """
        Return the list of available models.

        Returns:
            A dictionary of available models and their details.
        """
        return self.models

    def send_message(self, prompt, model=None, max_tokens=None):
        """
        Send a message to the specified model and get a response.

        Args:
            prompt: The user's message
            model: The model to use (defaults to default_model if None)
            max_tokens: Maximum tokens for the response

        Returns:
            The model's response text

        Raises:
            Exception: If there's an error in the API call
        """
        model = model or self.default_model

        # Prepare API call parameters
        params = {"model": model, "messages": [{"role": "user", "content": prompt}]}

        if max_tokens:
            params["max_tokens"] = max_tokens

        try:
            chat_completion = self.client.chat.completions.create(**params)
            return chat_completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

    def send_messages(self, messages, model=None, max_tokens=None):
        """
        Send messages to the specified model and get a response.

        Args:
            messages: List of message objects with role and content
            model: The model to use (defaults to default_model if None)
            max_tokens: Maximum tokens for the response

        Returns:
            The model's response text

        Raises:
            Exception: If there's an error in the API call
        """
        model = model or self.default_model

        # Prepare API call parameters
        params = {"model": model, "messages": messages}

        if max_tokens:
            params["max_tokens"] = max_tokens

        try:
            chat_completion = self.client.chat.completions.create(**params)
            return chat_completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")


def show_chatbot():
    with st.container():
        with st.columns([1, 11, 1])[1]:
            textArea = stylable_container(
                key="textArea",
                css_styles="""
                {
                    border: 1px solid rgba(255, 75, 75, 1);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                    background-color: white;
                    max-height: 450px;
                    overflow: scroll;
                }
                """,)
            with textArea:
                display_intro()
            try:
                # Initialize chatbot client
                if "chatbot_client" not in st.session_state:
                    try:
                        st.session_state.chatbot_client = ChatbotClient()
                    except ValueError as e:
                        st.warning(str(e))
                        st.stop()

                chatbot = st.session_state.chatbot_client

                # Initialize chat history and selected model
                if "messages" not in st.session_state:
                    st.session_state.messages = []

                # Display chat messages stored in history on app rerun
                with textArea:
                    for message in st.session_state.messages:
                        avatar = "assets/eand-logo/small/Red/e&-lockup_Enterprise_engl_vert_red_rgb-cropped.svg" if message["role"] == "assistant" else "🦔"
                        with st.chat_message(message["role"], avatar=avatar):
                            st.markdown(message["content"])

                # Handle user input
                with open('assets/styles/chat_input.css') as f:
                    css = f.read()

                st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
                if prompt := st.chat_input("Enter your prompt here...", max_chars=4200):
                    st.session_state.messages.append(
                        {"role": "user", "content": prompt}
                    )
                    response = chatbot.send_messages(st.session_state.messages)
                    st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                    st.rerun()
                    st.write(st.session_state.messages)

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}", icon="🚨")
