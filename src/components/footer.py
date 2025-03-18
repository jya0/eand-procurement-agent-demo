import streamlit as st


def streamlit_footer():
    st.divider()
    footer_col1, footer_col2, footer_col3 = st.columns(3)

    with footer_col1:
        st.text("AMPA - Automatic Market Procurement Agent")

    with footer_col2:
        st.text("Privacy Policy | Terms of Service")

    with footer_col3:
        st.text("© 2025 e& Enterprise")
