import streamlit as st
from src.components.footer import streamlit_footer
from src.components.roi import streamlit_roi


header_col1, header_col2 = st.columns([1, 3], gap="large")

with header_col1:
    st.image(
        image="assets/images/ampa-logos/ampa-square.png",
        use_container_width=True,
        caption="AMPA Logo",
    )

with header_col2:
    st.title("Streamline Your Procurement Process with AMPA")
    # st.title("Automatic Market Procurement Agent")
    st.text("Tired of spending up to 48 hours on manual procurement?")
    st.text(
        "Automatic Market Procurement Agent, or AMPA for short, communicates with suppliers for you and provides data-driven insights to save you time and money."
    )

st.divider()

# Main content in tabs
tabs = st.tabs(["Overview", "Features", "Benefits", "Get In Touch"])

# Overview Tab
with tabs[0]:
    col1, col2 = st.columns([2, 3], gap="large")

    with col1:
        st.header("Introduction", divider=True)
        st.text(
            "Retailers often face delays and inefficiencies due to time-consuming manual procurement tasks."
        )
        st.text(
            "AMPA integrates with leading supplier platforms like Alibaba to automate supplier searches, communications, and decision-making, delivering real-time insights through an intuitive dashboard."
        )

    with col2:
        st.image(
            image="assets/images/ampa-hla/HLA-AMPA-Investor-with-border-white.png",
            use_container_width=True,
            caption="Procurement Process Visualization",
        )

# Features Tab
with tabs[1]:
    st.header("Key Features", divider=True)

    with st.container():
        col1, col2 = st.columns(2, vertical_alignment="top")

        with col1:
            st.subheader("Criteria Based Search")
            with st.expander("", expanded=True):
                st.text(
                    "Deep search suppliers matching your criteria on B2B platforms such as Alibaba."
                )
                st.image(
                    # image="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGhrb3kyZG5qMG44YTY2Z2Q4MmxweHB2cjRnNDQ0MmtwcTEzcGJxZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wGKrkvHxZT6PVpw635/giphy.gif",
                    image="https://placehold.co/300x200",
                    caption="Supplier Search",
                )
            st.subheader("LLM-Based Recommendation Filter")
            with st.expander("", expanded=True):
                st.text(
                    "Filter search results to get top rated suppliers based on your chat."
                )
                st.image(
                    image="https://placehold.co/300x200", caption="AI Recommendation"
                )

        with col2:
            st.subheader("Agentic AI Communicator")
            with st.expander("", expanded=True):
                st.text(
                    "AI agentic system will contact and negotiate with new suppliers through email."
                )
                st.image(
                    image="https://placehold.co/300x200", caption="Email Automation"
                )
            st.subheader("SRM Dashboard")
            with st.expander("", expanded=True):
                st.text(
                    "Monitor procurement requests, supplier responses, and contract negotiation in one place."
                )
                st.image(
                    image="https://placehold.co/300x200", caption="Analytics Dashboard"
                )


# Benefits Tab
with tabs[2]:
    st.header("Benefits")

    benefit_cols = st.columns(4, vertical_alignment="top")

    benefits = [
        {
            "title": "Increased Efficiency",
            "description": "Significantly reduce the time and effort spent on procurement.",
            "icon": "https://placehold.co/100x100",
        },
        {
            "title": "Cost Savings",
            "description": "Optimize supplier selection to secure the best prices and terms.",
            "icon": "https://placehold.co/100x100",
        },
        {
            "title": "Better Decision-Making",
            "description": "Leverage data and AI insights to choose the right suppliers.",
            "icon": "https://placehold.co/100x100",
        },
        {
            "title": "Enhanced Relationships",
            "description": "Streamline communications for smoother, more productive interactions.",
            "icon": "https://placehold.co/100x100",
        },
    ]

    for i, benefit in enumerate(benefits):
        with benefit_cols[i]:
            st.image(benefit["icon"], width=100, caption=benefit["title"])
            st.subheader(benefit["title"], divider=True)
            st.text(benefit["description"])


    streamlit_roi()



# Get Started Tab
with tabs[3]:
    st.header("Get In Touch", divider=True)
    st.text("Ready to transform your procurement process?")

    with st.form("get_in_touch"):
        st.text_input("Company Name")
        st.text_input("Contact Person")
        st.text_input("Email")
        st.text_input("Phone")
        st.text_area("Specific Requirements")
        st.form_submit_button("Send")


streamlit_footer()
