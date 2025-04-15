import streamlit as st
from data.supliers import all_supplier
from src.components.ebay_api import EbayAPI
from src.components.cart import Cart
import math
from typing import List, Dict, Any, Callable, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CARDS_PER_PAGE = 6
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 200

# Constants
DEFAULT_PRICE_RANGE = (0, 100000)
PRICE_STEP = 100
DEFAULT_ITEMS_PER_PAGE = 10
ITEMS_PER_PAGE_OPTIONS = [10, 25, 50, 100]
MAX_RETRIES = 3

# Error messages
ERROR_MESSAGES = {
    "api_error": "An error occurred while searching eBay. Please try again later.",
    "invalid_category": "Invalid category selected. Please try again.",
    "invalid_subcategory": "Invalid subcategory selected. Please try again.",
    "search_failed": "Search failed. Please check your parameters and try again.",
    "session_error": "Session error. Please refresh the page and try again."
}

# Category mapping
CATEGORIES: Dict[str, List[str]] = {
    "All Categories": [],
    "Electronics": [
        "Computers & Tablets",
        "Cell Phones & Accessories",
        "Cameras & Photo",
        "TV, Video & Audio",
        "Video Games & Consoles",
        "Smart Home & Security"
    ],
    "Fashion": [
        "Men's Clothing",
        "Women's Clothing",
        "Shoes",
        "Jewelry & Watches",
        "Bags & Accessories",
        "Kids' Clothing"
    ],
    "Home & Garden": [
        "Furniture",
        "Home Décor",
        "Kitchen & Dining",
        "Bedding & Bath",
        "Garden & Outdoor",
        "Tools & Home Improvement"
    ],
    "Sports & Leisure": [
        "Exercise & Fitness",
        "Sports Equipment",
        "Outdoor Sports",
        "Team Sports",
        "Golf",
        "Cycling"
    ],
    "Toys & Hobbies": [
        "Action Figures",
        "Dolls & Bears",
        "Building Toys",
        "Games",
        "Model Trains",
        "RC Vehicles"
    ],
    "Automotive": [
        "Car Parts & Accessories",
        "Motorcycle Parts",
        "Truck Parts",
        "Tools & Equipment",
        "Car Electronics",
        "Tires & Wheels"
    ],
    "Health & Beauty": [
        "Fragrances",
        "Makeup",
        "Skin Care",
        "Hair Care",
        "Vitamins & Supplements",
        "Personal Care"
    ],
    "Jewelry & Watches": [
        "Fine Jewelry",
        "Fashion Jewelry",
        "Watches",
        "Loose Diamonds",
        "Loose Gemstones",
        "Jewelry Boxes"
    ],
    "Musical Instruments": [
        "Guitars",
        "Keyboards & Pianos",
        "Drums & Percussion",
        "Brass Instruments",
        "Woodwind Instruments",
        "Pro Audio Equipment"
    ],
    "Office Products": [
        "Office Furniture",
        "Office Electronics",
        "Office Supplies",
        "Printers & Scanners",
        "Presentation Equipment",
        "Shipping Supplies"
    ],
    "Pet Supplies": [
        "Dog Supplies",
        "Cat Supplies",
        "Fish Supplies",
        "Bird Supplies",
        "Reptile Supplies",
        "Small Animal Supplies"
    ],
    "Books & Magazines": [
        "Fiction Books",
        "Non-Fiction Books",
        "Textbooks",
        "Children's Books",
        "Magazines",
        "Audiobooks"
    ],
    "Industrial & Scientific": [
        "Lab Equipment",
        "Industrial Equipment",
        "Safety Equipment",
        "Electrical Equipment",
        "Material Handling",
        "Test Equipment"
    ]
}

# Condition mapping
CONDITION_MAP: Dict[str, str] = {
    "New": "NEW",
    "Used": "USED",
    "Refurbished": "REFURBISHED",
    "For parts or not working": "FOR_PARTS_OR_NOT_WORKING"
}

# Sort options mapping
SORT_MAP: Dict[str, str] = {
    "Best Match": "bestMatch",
    "Price: Low to High": "price",
    "Price: High to Low": "-price",
    "Time: ending soonest": "endTime",
    "Time: newly listed": "newlyListed"
}

ebay_api = EbayAPI()
cart = Cart()


if "cart_items" not in st.session_state:
    st.session_state.cart_items = []


def show_header(title: str, subtitle: str) -> None:
    with st.container():
        st.header(title, divider=True)
        st.caption(subtitle)


def show_image(image_path: str) -> None:
    try:
        st.image(image_path)
    except Exception:
        st.image("assets/images/placeholder.png")


def show_ebay_card(item: Dict[str, Any]) -> None:
    with st.container(border=True, height=600):
        st.header(f"👤 {item['seller']}")
            
        with st.container():
            col1, col2, col3 = st.columns([1, 8, 1], gap='small')
            with col2:
                show_image(item["image"])
        
        st.markdown(f"<h4>{item['title']}</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1], gap="small")
        with col1:
            try:
                price = float(item['price']) * 3.65
                st.metric("💰 Price", f"AED {price:.2f}")
            except (ValueError, TypeError):
                st.metric("💰 Price", "N/A")
        with col2:
            st.markdown(f"**{item['condition']}**")
            unique_key = f"add_to_cart_{item.get('id', hash(item['title']))}"
            
            # Check if item is already in cart
            item_id = item.get('id', hash(item['title']))
            is_in_cart = cart.is_item_in_cart(item_id)
            
            if is_in_cart:
                if st.button("Remove from cart", key=unique_key):
                    cart.remove_item(item_id)
                    st.rerun()
            else:
                if st.button("Add to cart", key=unique_key):
                    cart.add_item(item)
                    st.rerun()
        col1, col2 = st.columns([2, 1])                    
        with col1:    
            st.markdown(f"[View on eBay]({item['url']})")
        with col2:
            status = "✅ Verified" if item.get("verified", False) else "❌ Not Verified"
            st.markdown(f"**{status}**")


def show_supplier_card(supplier: Dict[str, Any]) -> None:
    with st.container(border=True, height=400):
        with st.container():
            st.header(supplier["name"])
            show_image(supplier["image"])
        with st.container():
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
    """Sort items based on the selected sort option."""
    try:
        # Get the sort key from SORT_MAP, defaulting to "Best Match"
        sort_key = SORT_MAP.get(sort_by, "bestMatch")
        
        # Sort the items based on the selected criteria
        if sort_key == "price":
            return sorted(items, key=lambda x: float(x.get("price", 0)))
        elif sort_key == "-price":
            return sorted(items, key=lambda x: -float(x.get("price", 0)))
        elif sort_key == "endTime":
            return sorted(items, key=lambda x: x.get("endTime", ""))
        elif sort_key == "newlyListed":
            return sorted(items, key=lambda x: x.get("listingDate", ""))
        else:  # bestMatch
            return items
    except Exception as e:
        logger.error(f"Error sorting items: {str(e)}")
        return items


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
                min_value=0,
                max_value=1000,
                value=0,
                step=1,
                format="%d",
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


def validate_category(category: str, subcategory: Optional[str] = None) -> bool:
    """Validate if the selected category and subcategory are valid."""
    try:
        if category not in CATEGORIES:
            logger.error(f"Invalid category: {category}")
            return False
        
        if subcategory and category != "All Categories":
            if subcategory not in CATEGORIES[category]:
                logger.error(f"Invalid subcategory: {subcategory} for category: {category}")
                return False
        
        return True
    except Exception as e:
        logger.error(f"Error validating category: {str(e)}")
        return False


def handle_search_error(error: Exception) -> None:
    """Handle search errors and display appropriate messages."""
    error_message = str(error).lower()
    
    if "api" in error_message:
        st.error(ERROR_MESSAGES["api_error"])
    elif "category" in error_message:
        st.error(ERROR_MESSAGES["invalid_category"])
    elif "subcategory" in error_message:
        st.error(ERROR_MESSAGES["invalid_subcategory"])
    else:
        st.error(ERROR_MESSAGES["search_failed"])
    
    logger.error(f"Search error: {str(error)}")


def initialize_session_state() -> None:
    """Initialize session state variables for category selection with validation."""
    try:
        if "selected_category" not in st.session_state:
            st.session_state.selected_category = "All Categories"
        if "selected_subcategory" not in st.session_state:
            st.session_state.selected_subcategory = None
            
        # Validate existing session state
        if not validate_category(st.session_state.selected_category, st.session_state.selected_subcategory):
            st.session_state.selected_category = "All Categories"
            st.session_state.selected_subcategory = None
            st.warning("Invalid category selection was reset.")
    except Exception as e:
        logger.error(f"Session state initialization error: {str(e)}")
        st.error(ERROR_MESSAGES["session_error"])


def get_button_text() -> str:
    """Generate the text for the category selection button based on current selection."""
    try:
        if st.session_state.selected_category == "All Categories":
            return "Select Category"
        
        if not validate_category(st.session_state.selected_category, st.session_state.selected_subcategory):
            return "Select Category"
        
        text = st.session_state.selected_category
        if st.session_state.selected_subcategory:
            text += f" > {st.session_state.selected_subcategory}"
        return text
    except Exception as e:
        logger.error(f"Error getting button text: {str(e)}")
        return "Select Category"


def build_search_filters(condition: str, price_range: int) -> List[str]:
    """Build the filter string for the eBay API search with validation."""
    try:
        filters = []
        if condition != "Any" and condition in CONDITION_MAP:
            filters.append(f"conditions:{{{CONDITION_MAP[condition]}}}")
        if price_range < DEFAULT_PRICE_RANGE[1]:
            filters.append(f"price:[..{price_range}]")
        return filters
    except Exception as e:
        logger.error(f"Error building filters: {str(e)}")
        return []


def build_search_query() -> str:
    """Build the search query using selected category and subcategory with validation."""
    try:
        if not validate_category(st.session_state.selected_category, st.session_state.selected_subcategory):
            return ""
            
        if st.session_state.selected_category == "All Categories":
            return ""
        
        query = st.session_state.selected_category
        if st.session_state.selected_subcategory:
            query += f" {st.session_state.selected_subcategory}"
        return query
    except Exception as e:
        logger.error(f"Error building search query: {str(e)}")
        return ""


@st.dialog("Select Category")
def category_dialog() -> None:
    """Display the category selection dialog with validation."""
    try:
        st.markdown("### Select Category")
        
        # Main category selection
        main_category = st.selectbox(
            "Main Category",
            options=list(CATEGORIES.keys()),
            index=list(CATEGORIES.keys()).index(st.session_state.selected_category),
            key="dialog_main_category_select"
        )
        
        # Subcategory selection
        subcategory = None
        if main_category != "All Categories" and CATEGORIES[main_category]:
            subcategory = st.selectbox(
                "Subcategory",
                options=CATEGORIES[main_category],
                index=0 if not st.session_state.selected_subcategory else 
                      CATEGORIES[main_category].index(st.session_state.selected_subcategory),
                key="dialog_subcategory_select"
            )
        
        # Dialog buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Apply", key="dialog_apply_category"):
                if validate_category(main_category, subcategory):
                    st.session_state.selected_category = main_category
                    st.session_state.selected_subcategory = subcategory
                    st.rerun()
                else:
                    st.error("Invalid category selection. Please try again.")
        with col2:
            if st.button("Cancel", key="dialog_cancel_category"):
                st.rerun()
    except Exception as e:
        logger.error(f"Error in category dialog: {str(e)}")
        st.error("An error occurred in the category selection. Please try again.")


def perform_search(search_query: str, filters: List[str], sort_by: str, items_per_page: int) -> List[Dict[str, Any]]:
    """Perform the eBay search with retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            items = ebay_api.search_items(
                search_query,
                limit=items_per_page,
                sort=SORT_MAP[sort_by],
                filters=",".join(filters) if filters else None
            )
            return [ebay_api.format_item(item) for item in items]
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise e
            logger.warning(f"Search attempt {attempt + 1} failed: {str(e)}")
            continue


def show_ebay_search_form() -> None:
    """Display the eBay search form with category selection and filters."""
    try:
        initialize_session_state()
        
        with st.container():
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                st.markdown("Choose Category")
                if st.button(get_button_text(), key="main_category_button"):
                    category_dialog()
                
                condition = st.selectbox(
                    "Condition",
                    options=["Any", "New", "Used", "Refurbished", "For parts or not working"],
                    index=0,
                    key="main_condition_select"
                )
                location = st.selectbox(
                    "Location",
                    options=["Worldwide", "United States", "Europe", "Asia", "Australia"],
                    index=0,
                    key="main_location_select"
                )
                
            with col2:
                price_range = st.slider(
                    "Maximum Price (DHS)",
                    min_value=DEFAULT_PRICE_RANGE[0],
                    max_value=DEFAULT_PRICE_RANGE[1],
                    value=DEFAULT_PRICE_RANGE[1],
                    step=PRICE_STEP,
                    format="%d",
                    key="main_price_slider"
                )
                sort_by = st.selectbox(
                    "Sort by",
                    options=list(SORT_MAP.keys()),
                    index=0,
                    key="main_sort_select"
                )
                items_per_page = st.selectbox(
                    "Items per page",
                    options=ITEMS_PER_PAGE_OPTIONS,
                    index=0,
                    key="main_items_per_page_select"
                )
                
                _, col_right = st.columns([5, 1], gap="small")
                with col_right:
                    if st.button("Search eBay", key="main_search_button", type="primary"):
                        try:
                            st.session_state.page = 0
                            
                            filters = build_search_filters(condition, price_range)
                            search_query = build_search_query()
                            
                            items = perform_search(search_query, filters, sort_by, items_per_page)
                            
                            st.session_state.search_results = items
                            st.session_state.has_search = True
                        except Exception as e:
                            handle_search_error(e)
    except Exception as e:
        logger.error(f"Error in search form: {str(e)}")
        st.error("An unexpected error occurred. Please try again later.")


def show_search_results() -> None:
    """Display the search results with sorting options."""
    st.header("Suppliers Listings")
    
    if "page" not in st.session_state:
        st.session_state.page = 0
    if "has_search" not in st.session_state:
        st.session_state.has_search = False
    if "search_results" not in st.session_state:
        st.session_state.search_results = []
        
    sort_by = st.selectbox("Sort by", options=list(SORT_MAP.keys()), index=0)
    
    items = st.session_state.search_results if st.session_state.has_search and st.session_state.search_results else all_supplier
    sorted_items = sort_items(items, sort_by)
    
    total_pages = math.ceil(len(sorted_items) / CARDS_PER_PAGE)
    start_idx = st.session_state.page * CARDS_PER_PAGE
    current_items = sorted_items[start_idx:start_idx + CARDS_PER_PAGE]
    
    show_items_grid(current_items)
    show_pagination(st.session_state.page, total_pages)


def show_cart() -> None:
    """Display the shopping cart contents"""
    cart.display()
