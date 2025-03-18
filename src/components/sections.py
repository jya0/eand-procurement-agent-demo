import streamlit as st
from src.components.card import shop_card
from src.components.chatbox import chatbox
from data.supliers import all_supplier
import math


def section_header(headerText: str, captionText: str):
    with st.container():
        st.header(headerText, divider=True)
        st.caption(captionText)

def section_search():
    with st.form(key="search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name")
            time_input = st.time_input("Time")
            location = st.text_input("Location")
        
        with col2:
            price = st.slider("Price", min_value=0.0, max_value=1000.0, 
                            value=0.0, step=0.01, format="%.2f")
            verify = st.radio("Verify", options=["Yes", "No"])
            age = st.number_input("Age", min_value=0)
        
        submitted = st.form_submit_button("Search")
        

def section_search_results():
    supplier = all_supplier

    st.header("Suppliers Listings")  # Fixed typo
    
    # Pagination controls
    if 'page' not in st.session_state:
        st.session_state.page = 0
        
    cards_per_page = 6  # 6 cards per page (2 rows of 3)
    rows_per_page = cards_per_page // 3  # 2 rows per page
    total_pages = math.ceil(len(supplier) / cards_per_page)
    
    # Get current page suppliers
    start_idx = st.session_state.page * cards_per_page
    end_idx = start_idx + cards_per_page
    current_suppliers = supplier[start_idx:end_idx]

    with st.container(border=True):
        # Display current page cards
        for i in range(0, len(current_suppliers), 3):
            cols = st.columns(3)
            row_suppliers = current_suppliers[i:i+3]
            
            for col, sup in zip(cols, row_suppliers):
                with col:
                    with st.container(border=True):
                        st.image(sup["image"])
                        st.subheader(sup["name"])
                        st.caption(f"📍 {sup['location']}")
                        
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.metric("🚚 Delivery Time", sup["delivery_time"])
                        with col2:
                            status = "✅ Verified" if sup["verified"] else "❌ Not Verified"
                            st.markdown(f"**{status}**")
                        
                        st.markdown(f"⭐ **Rating:** {sup['rating']}/5.0")
        
        # Pagination controls at bottom
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            prev, _, next = st.columns([1, 2, 1])
            
            with prev:
                if st.button("⬅️ Previous", disabled=st.session_state.page == 0):
                    st.session_state.page -= 1
                    st.rerun()
            
            with next:
                if st.button("Next ➡️", disabled=st.session_state.page >= total_pages - 1):
                    st.session_state.page += 1
                    st.rerun()
            
            st.caption(f"Page {st.session_state.page + 1} of {total_pages}")