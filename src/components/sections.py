import streamlit as st
from data.supliers import all_supplier
import math


def section_header(headerText: str, captionText: str):
    with st.container():
        st.header(headerText, divider=True)
        st.caption(captionText)


def section_search():
    with st.form(key="search_form"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            name = st.text_input("Name")
            time_input = st.time_input("Time")
            location = st.text_input("Location")

        with col2:
            price = st.slider(
                "Price",
                min_value=0.0,
                max_value=1000.0,
                value=0.0,
                step=0.01,
                format="%.2f",
            )
            verify = st.radio("Verify", options=["Yes", "No"])
            age = st.number_input("Age", min_value=0)

        submitted = st.form_submit_button("Search")


def display_supplier_card(supplier):
    """Display a single supplier card with details."""
    with st.container(border=True):
        st.image(supplier["image"])
        st.subheader(supplier["name"])
        st.caption(f"📍 {supplier['location']}")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.metric("🚚 Delivery Time", supplier["delivery_time"])
        with col2:
            status = "✅ Verified" if supplier["verified"] else "❌ Not Verified"
            st.markdown(f"**{status}**")

        st.markdown(f"⭐ **Rating:** {supplier['rating']}/5.0")


def display_suppliers_grid(suppliers):
    """Display a grid of supplier cards (3 cards per row)."""
    with st.container(border=True):
        for i in range(0, len(suppliers), 3):
            cols = st.columns(3)
            row_suppliers = suppliers[i : i + 3]

            for col, supplier in zip(cols, row_suppliers):
                with col:
                    display_supplier_card(supplier)


def setup_pagination(total_pages):
    """Display pagination controls (Previous and Next buttons)."""
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


def section_search_results():
    """Main function to display the supplier listings with pagination."""
    supplier = all_supplier

    st.header("Suppliers Listings")

    if "page" not in st.session_state:
        st.session_state.page = 0

    cards_per_page = 6
    total_pages = math.ceil(len(supplier) / cards_per_page)

    start_idx = st.session_state.page * cards_per_page
    end_idx = start_idx + cards_per_page
    current_suppliers = supplier[start_idx:end_idx]


    display_suppliers_grid(current_suppliers)

    setup_pagination(total_pages)
