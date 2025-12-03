# ui/main.py
import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path
import io

from core.engine import LibraryEngine
from core.models import Book
from utils.helpers import ensure_sample_data, short_id, COLLEGE_NAME, COLLEGE_EMAIL

# ---------------------- CSS Loader ----------------------
def _local_css():
    st.markdown("""
        <style>
        .title {
            font-size: 2.3rem;
            font-weight: 700;
            color: #b91c1c;
            margin-bottom: -10px;
        }
        .subtitle {
            font-size: 1rem;
            color: #752424;
            opacity: 0.85;
        }
        .section-header {
            color: #b91c1c;
            font-weight: 700;
            font-size: 1.6rem;
            margin-top: 1rem;
            margin-bottom: 0.4rem;
        }
        div.stButton>button {
            background-color: #b91c1c !important;
            color: white !important;
            border-radius: 6px;
            padding: 8px 16px;
        }
        div.stButton>button:hover {
            background-color: #7f0f0f !important;
        }
        .metric-box {
            padding: 15px;
            border-radius: 12px;
            background-color: #fff0f0;
            border: 1px solid #f0dada;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)


# Helper map: item_id → title
def id_to_title_map():
    books = LibraryEngine.list_books()
    return {b.item_id: b.title for b in books}


# ---------------------- MAIN UI ----------------------
def main_ui():
    _local_css()
    ensure_sample_data()

    st.markdown(f"""
        <h1 class='title'>📚 Library Management Portal</h1>
        <p class='subtitle'>Welcome! Contact us at <b>{COLLEGE_EMAIL}</b></p>
    """, unsafe_allow_html=True)

    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["About", "Dashboard", "Catalog", "Add Book", "Users", "Issue Book", "Reserve Book"]
    )

    if page == "About":
        about_page()
    elif page == "Dashboard":
        dashboard_page()
    elif page == "Catalog":
        catalog_page()
    elif page == "Add Book":
        add_book_page()
    elif page == "Users":
        users_page()
    elif page == "Issue Book":
        issue_page()
    elif page == "Reserve Book":
        reserve_page()


# ---------------------- ABOUT PAGE ----------------------
def about_page():
    st.markdown("<div class='section-header'>About This Portal</div>", unsafe_allow_html=True)

    st.markdown("""
This Library Management Portal is designed for **Indian engineering colleges** to handle all day-to-day library operations.

### ⭐ What this portal offers:
- Browse hundreds of engineering textbooks  
- Search & filter books  
- Add, edit, delete books  
- Issue books to students  
- Reserve books  
- Return books  
- Automatic overdue tracking  
- Auto fine calculation  
- Dashboard with full library statistics  
- Export user & loan data to CSV  
- Track borrowed & reserved items easily  

Built to be **simple, beautiful, and beginner-friendly**.
    """)


# ---------------------- DASHBOARD ----------------------
def dashboard_page():
    st.markdown("<div class='section-header'>Dashboard</div>", unsafe_allow_html=True)

    stats = LibraryEngine.counts()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Titles", stats["total_titles"])
    c2.metric("Total Copies", stats["total_copies"])
    c3.metric("Students", stats["total_users"])

    c4, c5, c6 = st.columns(3)
    c4.metric("Borrowed Items", stats["active_loans"])
    c5.metric("Reservations", stats["reservations"])
    c6.metric("Overdue Loans", stats["overdue_count"])


# ---------------------- CATALOG PAGE ----------------------
def catalog_page():
    st.markdown("<div class='section-header'>Book Catalog</div>", unsafe_allow_html=True)
    books = LibraryEngine.list_books()

    q = st.text_input("Search Books (Title / Author)")
    cat = st.selectbox("Filter by Category", ["All"] + sorted({b.category for b in books}))

    filtered = [
        b for b in books
        if (not q or q.lower() in b.tit
