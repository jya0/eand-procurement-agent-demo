import streamlit as st
from src.components.sections import section_header, section_search, section_search_results
from src.components.chatbox import chatbox

# Configure page settings
# st.set_page_config(
#     page_title="Shop & Chat Interface",
#     page_icon="assets/eand-logo/small/White/e&-lockup_Enterprise_engl_vert_White_rgb.svg",
#     layout="wide"
# )

st.title("How It Works")

section_header(
    "Input Your Criteria",
    "Use our simple form to specify product requirements, budget, and delivery preferences."
)

section_search()

section_header(
    "Search for Suppliers",
    "AMPA searches Alibaba's vast database to find matching suppliers instantly."
)

section_search_results()

section_header(
    "Evaluate with Chatbot",
    "Ask our AI chatbot for recommendations or details, like \"Which supplier offers the best price-to-quality ratio?\""
)
with st.container():
    chatbox()

section_header(
    "Automate Communications",
    "Select suppliers and let AMPA handle outreach and follow-ups via automated emails."
)

section_header(
    "Monitor and Finalize",
    "Track communications and negotiation progress in the real-time dashboard, then finalize deals with ease."
)
