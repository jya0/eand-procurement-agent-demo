import streamlit as st
from src.components.sections import show_header, show_search_form, show_search_results, show_ebay_search_form
from src.components.footer import streamlit_footer
from src.components.chatbot import show_chatbot


st.title("How It Works")

st.divider()

# section_header(
#     "Input Your Criteria",
#     "Use our simple form to specify product requirements, budget, and delivery preferences."
# )

st.header("Input Your Criteria", divider=True)
with st.expander("Use our simple form to specify product requirements, budget, and delivery preferences."):
    # show_search_form()
    show_ebay_search_form()

# section_header(
#     "Search for Suppliers",
#     "AMPA searches Alibaba's vast database to find matching suppliers instantly."
# )

st.header("Search for Suppliers", divider=True)
# with st.expander("AMPA searches Alibaba's vast database to find matching suppliers instantly."):
show_search_results()


# section_header(
#     "Evaluate with Chatbot",
#     "Ask our AI chatbot for recommendations or details, like \"Which supplier offers the best price-to-quality ratio?\""
# )

st.header("Evaluate with Chatbot", divider=True)
with st.expander("Ask our AI chatbot for recommendations or details, like \"Which supplier offers the best price-to-quality ratio?\""):
    show_chatbot()

show_header(
    "Automate Communications",
    "Select suppliers and let AMPA handle outreach and follow-ups via automated emails."
)

show_header(
    "Monitor and Finalize",
    "Track communications and negotiation progress in the real-time dashboard, then finalize deals with ease."
)


streamlit_footer()
