import streamlit as st
from data.supliers import all_supplier
from src.components.ebay_api import EbayAPI
import math
from typing import List, Dict, Any, Callable

CARDS_PER_PAGE = 6
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 200

SORT_OPTIONS = {
    "Price (Low to High)": lambda x: float(x.get("price", 0)),
    "Price (High to Low)": lambda x: -float(x.get("price", 0)),
    "Rating (High to Low)": lambda x: -float(x.get("rating", 0)),
    "Delivery Time (Fastest)": lambda x: int(x.get("delivery_time", "0-0").split("-")[0])
}

ebay_api = EbayAPI()

def show_header(title: str, subtitle: str) -> None:
    with st.container():
        st.header(title, divider=True)
        st.caption(subtitle)

def show_image(image_path: str) -> None:
    try:
        st.image(image_path, use_container_width=True)
    except Exception:
        st.image("assets/images/placeholder.png")

def show_ebay_card(item: Dict[str, Any]) -> None:
    with st.container(border=True):
        with st.container():
            st.header(f"👤 {item['seller']}")
            show_image(item["image"])
        
        with st.container():
            st.subheader(item["title"])
            
            col1, col2 = st.columns([2, 1], gap="small")
            with col1:
                try:
                    price = float(item['price']) * 3.65
                    st.metric("💰 Price", f"AED {price:.2f}")
                except (ValueError, TypeError):
                    st.metric("💰 Price", "N/A")
            with col2:
                st.markdown(f"**{item['condition']}**")
                
            st.markdown(f"[View on eBay]({item['url']})")

def show_supplier_card(supplier: Dict[str, Any]) -> None:
    with st.container(border=True):
        with st.container():
            show_image(supplier["image"])
        with st.container():
            st.subheader(supplier["name"])
            st.caption(f"📍 {supplier['location']}")
            
            col1, col2 = st.columns([2, 1], gap="small")
            with col1:
                st.metric("🚚 Delivery Time", supplier["delivery_time"])
            with col2:
                status = "✅ Verified" if supplier["verified"] else "❌ Not Verified"
                st.markdown(f"**{status}**")
                st.metric("💰 Price", f"${supplier['price']:.2f}")
                
            st.markdown(f"⭐ **Rating:** {supplier['rating']}/5.0")

def show_items_grid(items: List[Dict[str, Any]]) -> None:
    with st.container(border=True):
        for i in range(0, len(items), 3):
            cols = st.columns(3)
            row_items = items[i:i + 3]
            
            for col, item in zip(cols, row_items):
                with col:
                    show_ebay_card(item) if "title" in item else show_supplier_card(item)

def show_pagination(current_page: int, total_pages: int) -> None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        prev, _, next = st.columns([1, 2, 1])
        
        with prev:
            if st.button("⬅️ Previous", disabled=current_page == 0):
                st.session_state.page -= 1
                st.rerun()
                
        with next:
            if st.button("Next ➡️", disabled=current_page >= total_pages - 1):
                st.session_state.page += 1
                st.rerun()
                
        st.caption(f"Page {current_page + 1} of {total_pages}")

def sort_items(items: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
    sort_key = SORT_OPTIONS.get(sort_by, SORT_OPTIONS["Price (Low to High)"])
    return sorted(items, key=sort_key)

def show_search_form() -> None:
    with st.form(key="search_form"):
        col1, col2 = st.columns(2, gap="large")
        
        with col1:  
            search_query = st.text_input("Product name")
            st.time_input("Expected shipment time")
            st.text_input("Location")
            
        with col2:
            max_price = st.slider(
                "Price",
                min_value=0.0,
                max_value=1000.0,
                value=0.0,
                step=0.01,
                format="%.2f",
            )
            st.radio("Verify", options=["Yes", "No"])
            st.number_input("Age", min_value=0)
            
        if st.form_submit_button("Search") and search_query:
            try:
                st.session_state.page = 0
                items = ebay_api.search_items(search_query)
                st.session_state.search_results = [ebay_api.format_item(item) for item in items]
                st.session_state.has_search = True
            except Exception as e:
                st.error(f"Error searching eBay: {str(e)}")

def show_ebay_search_form() -> None:
    with st.form(key="ebay_search_form"):
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            category = st.selectbox(
                "Category",
                options=[
                    "All Categories",
                    "Electronics",
                    "Fashion",
                    "Home & Garden",
                    "Sports & Leisure",
                    "Toys & Hobbies",
                    "Automotive",
                    "Health & Beauty",
                    "Jewelry & Watches",
                    "Musical Instruments",
                    "Office Products",
                    "Pet Supplies",
                    "Books & Magazines",
                    "Art & Collectibles",
                    "Musical Instruments",
                    "Industrial & Scientific"
                ],
                index=0
            )
            condition = st.selectbox(
                "Condition",
                options=["Any", "New", "Used", "Refurbished", "For parts or not working"],
                index=0
            )
            location = st.selectbox(
                "Location",
                options=["Worldwide", "United States", "Europe", "Asia", "Australia"],
                index=0
            )
            
        with col2:
            price_range = st.slider(
                "Maximum Price (DHS)",
                min_value=0.0,
                max_value=100000.0,
                value=100000.0,
                step=1000.0,
                format="%.2f",
            )
            sort_by = st.selectbox(
                "Sort by",
                options=["Best Match", "Price: Low to High", "Price: High to Low", "Time: ending soonest", "Time: newly listed"],
                index=0
            )
            items_per_page = st.selectbox(
                "Items per page",
                options=[10, 25, 50, 100],
                index=0
            )
            
            # Add columns for the submit button
            _, col_right = st.columns([5, 1], gap="small")
            with col_right:
                submit_button = st.form_submit_button("Search eBay")
            
        if submit_button:
            try:
                st.session_state.page = 0
                
                # Convert condition to eBay API format
                condition_map = {
                    "New": "NEW",
                    "Used": "USED",
                    "Refurbished": "REFURBISHED",
                    "For parts or not working": "FOR_PARTS_OR_NOT_WORKING"
                }
                
                # Convert sort option to eBay API format
                sort_map = {
                    "Best Match": "bestMatch",
                    "Price: Low to High": "price",
                    "Price: High to Low": "-price",
                    "Time: ending soonest": "endTime",
                    "Time: newly listed": "newlyListed"
                }
                
                # Build filter string
                filters = []
                if condition != "Any":
                    filters.append(f"conditions:{{{condition_map[condition]}}}")
                if price_range < 100000.0:
                    filters.append(f"price:[..{price_range}]")
                
                # Use category as search query if not "All Categories"
                search_query = category if category != "All Categories" else ""
                
                items = ebay_api.search_items(
                    search_query,
                    limit=items_per_page,
                    sort=sort_map[sort_by],
                    filters=",".join(filters) if filters else None
                )
                
                st.session_state.search_results = [ebay_api.format_item(item) for item in items]
                st.session_state.has_search = True
            except Exception as e:
                st.error(f"Error searching eBay: {str(e)}")

def show_search_results() -> None:
    st.header("Suppliers Listings")
    
    if "page" not in st.session_state:
        st.session_state.page = 0
    if "has_search" not in st.session_state:
        st.session_state.has_search = False
    if "search_results" not in st.session_state:
        st.session_state.search_results = []
        
    sort_by = st.selectbox("Sort by", options=list(SORT_OPTIONS.keys()), index=0)
    
    items = st.session_state.search_results if st.session_state.has_search and st.session_state.search_results else all_supplier
    sorted_items = sort_items(items, sort_by)
    
    total_pages = math.ceil(len(sorted_items) / CARDS_PER_PAGE)
    start_idx = st.session_state.page * CARDS_PER_PAGE
    current_items = sorted_items[start_idx:start_idx + CARDS_PER_PAGE]
    
    show_items_grid(current_items)
    show_pagination(st.session_state.page, total_pages)