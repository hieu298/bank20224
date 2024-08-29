import streamlit as st
st.set_page_config(
    page_title="Your Page Title",
    layout="wide",
    initial_sidebar_state="expanded"
)
# --- PAGE SETUP ---
about_page = st.Page(
    "views/about_me.py",
    title="Về chúng tôi",
    icon=":material/account_circle:",
    default=True,
)
project_1_page = st.Page(
    "views/sales_dashboard.py",
    title="Dữ liệu tài chính",
    icon=":material/bar_chart:",
)
project_2_page = st.Page(
    "views/compare.py",
    title="Biểu đồ tài chính",
    icon=":material/smart_toy:",
)
project_3_page = st.Page(
    "views/chatbot.py",
    title="News",
    icon=":material/smart_toy:",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [about_page],
        "Projects": [project_1_page, project_2_page,project_3_page],
    }
)


# --- SHARED ON ALL PAGES ---
st.sidebar.markdown("Tham gia với chúng tôi tại ✉️ .[TienDalio](https://www.youtube.com/@tiendalio7734)")

# --- RUN NAVIGATION ---
pg.run()

