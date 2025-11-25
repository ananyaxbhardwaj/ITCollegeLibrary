# app.py
import streamlit as st
from ui import main

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Library Management Portal",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- RUN THE APP ----------------
if __name__ == "__main__":
    main.main_ui()
