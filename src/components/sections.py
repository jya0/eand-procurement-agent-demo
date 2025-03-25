import streamlit as st
from data.supliers import all_supplier
import math
from typing import List, Dict, Any, Callable

# Constants
CARDS_PER_PAGE: int = 6
SORT_OPTIONS: Dict[str, Callable[[Dict[str, Any]], Any]] = {
    "Price (Low to High)": lambda x: x["price"],
    "Price (High to Low)": lambda x: -x["price"],
    "Rating (High to Low)": lambda x: -x["rating"],
    "Delivery Time (Fastest)": lambda x: int(x["delivery_time"].split("-")[0])
}

def section_header(header_text: str, caption_text: str) -> None:
    """
    Display a section header with a caption.
    
    Args:
        header_text (str): The main header text
        caption_text (str): The caption text below the header
    """
    with st.container():
        st.header(header_text, divider=True)
        st.caption(caption_text)

def section_search() -> None:
    """Display a search form with various input fields."""
    with st.form(key="search_form"):
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.text_input("Product name")
            st.time_input("Expected shipment time")
            st.text_input("Location")
            
        with col2:
            st.slider(
                "Price",
                min_value=0.0,
                max_value=1000.0,
                value=0.0,
                step=0.01,
                format="%.2f",
            )
            st.radio("Verify", options=["Yes", "No"])
            st.number_input("Age", min_value=0)
            
        st.form_submit_button("Search")

def display_supplier_card(supplier: Dict[str, Any]) -> None:
    """
    Display a single supplier card with all relevant information.
    
    Args:
        supplier (Dict[str, Any]): Dictionary containing supplier information
    """
    with st.container(border=True):
        # Display supplier image and name
        st.image(supplier["image"])
        st.subheader(supplier["name"])
        st.caption(f"📍 {supplier['location']}")
        
        # Display metrics in two columns
        col1, col2 = st.columns([2, 1], gap="small")
        with col1:
            st.metric("🚚 Delivery Time", supplier["delivery_time"])
        with col2:
            status = "✅ Verified" if supplier["verified"] else "❌ Not Verified"
            st.markdown(f"**{status}**")
            st.metric("💰 Price", f"${supplier['price']:.2f}")
            
        st.markdown(f"⭐ **Rating:** {supplier['rating']}/5.0")

def display_suppliers_grid(suppliers: List[Dict[str, Any]]) -> None:
    """
    Display a grid of supplier cards (3 cards per row).
    
    Args:
        suppliers (List[Dict[str, Any]]): List of supplier dictionaries
    """
    with st.container(border=True):
        for i in range(0, len(suppliers), 3):
            cols = st.columns(3)
            row_suppliers = suppliers[i:i + 3]
            
            for col, supplier in zip(cols, row_suppliers):
                with col:
                    display_supplier_card(supplier)


def setup_pagination(total_pages: int) -> None:
    """
    Display pagination controls for navigating through pages.
    
    Args:
        total_pages (int): Total number of pages available
    """
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

def get_sorted_suppliers(suppliers: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
    """
    Sort suppliers based on selected criteria.
    
    Args:
        suppliers (List[Dict[str, Any]]): List of supplier dictionaries
        sort_by (str): Sorting criteria from SORT_OPTIONS
        
    Returns:
        List[Dict[str, Any]]: Sorted list of suppliers
    """
    sort_key = SORT_OPTIONS.get(sort_by, SORT_OPTIONS["Price (Low to High)"])
    return sorted(suppliers, key=sort_key)

def section_search_results() -> None:
    """Display the supplier listings with pagination and sorting options."""
    st.header("Suppliers Listings")
    
    if "page" not in st.session_state:
        st.session_state.page = 0
        
    sort_by = st.selectbox(
        "Sort by",
        options=list(SORT_OPTIONS.keys()),
        index=0
    )
    
    sorted_suppliers = get_sorted_suppliers(all_supplier, sort_by)
    total_pages = math.ceil(len(sorted_suppliers) / CARDS_PER_PAGE)
    start_idx = st.session_state.page * CARDS_PER_PAGE
    end_idx = start_idx + CARDS_PER_PAGE
    current_suppliers = sorted_suppliers[start_idx:end_idx]
    
    display_suppliers_grid(current_suppliers)
    setup_pagination(total_pages)