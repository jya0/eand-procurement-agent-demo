import streamlit as st
from streamlit_navigation_bar import st_navbar


st.set_page_config(
    layout="wide",
    page_icon="assets/eand-logo/small/Red/e&-lockup_Enterprise_engl_vert_red_rgb-cropped.svg"
)


ALL_PAGES = [
    st.Page(
        page="app_pages/Home_.py",
        title="AMPA - Automatic Market Procurement Agent"
        ),
    st.Page(
        page="app_pages/Demo_.py",
        title="Shop & Chat Interface"
        )
]


ALL_PAGES_TITLE_KEY = [
    "Home",
    "Demo"
]


stNavbarOut = st_navbar(
    ALL_PAGES_TITLE_KEY,
    logo_path="assets/eand-logo/small/White/e&-lockup_Enterprise_engl_vert_White_rgb-cropped.svg",
    logo_page=None,
    options={
        "show_menu": False,
        "use_padding": True,
    },
    styles={
        "nav": {
            "justify-content": "left",
            "margin-bottom": "40 rem",
        },
        "span": {
            "border-radius": "0.5rem",
            "padding": "0.625rem",
        },
        "active": {
            "background-color": "rgba(255, 255, 255, 0.25)",
        },
        "hover": {
            "background-color": "rgba(255, 255, 255, 0.1)",
        },
    },
    key="navBarMain",
)

st.container(height=10, border=False)



def getPage(navBarPageSelected: str):
    for i in range(0, len(ALL_PAGES_TITLE_KEY)):
        if navBarPageSelected == ALL_PAGES_TITLE_KEY[i]:
            return (ALL_PAGES[i])
    return (None)


if st.session_state["navBarMain"] and st.session_state["navBarMain"][0]:
    # st.write(st.session_state["navBarMain"][0])
    pageToSwitch = getPage(st.session_state["navBarMain"][0])
    # st.write(pageToSwitch)
    if pageToSwitch:
        st.session_state["navBarMain"][0] = None
        st.switch_page(pageToSwitch)


pg = st.navigation(ALL_PAGES)


pg.run()
