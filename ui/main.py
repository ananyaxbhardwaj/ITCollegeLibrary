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

    # Loan tracking removed — nothing to display here.


# ---------------------- CATALOG PAGE ----------------------
def catalog_page():
    st.markdown("<div class='section-header'>Book Catalog</div>", unsafe_allow_html=True)
    books = LibraryEngine.list_books()

    q = st.text_input("Search Books (Title / Author)")
    cat = st.selectbox("Filter by Category", ["All"] + sorted({b.category for b in books}))

    filtered = [
        b for b in books
        if (not q or q.lower() in b.title.lower() or q.lower() in b.author.lower())
        and (cat == "All" or b.category == cat)
    ]

    df = pd.DataFrame([{
        "Display ID": short_id(b.item_id),
        "Title": b.title,
        "Author": b.author,
        "Publisher": b.publisher,
        "Year": b.year,
        "Category": b.category,
        "Copies": b.copies,
    } for b in filtered])

    st.dataframe(df, use_container_width=True)

    # Select Book
    st.markdown("### Edit or Delete Book")
    # Use selectbox with objects and format_func so we get the Book back directly
    select = st.selectbox(
        "Choose a Book",
        options=filtered,
        format_func=lambda b: f"{short_id(b.item_id)} — {b.title}" if b else "",
    )

    # Use session state to show edit modal after Edit button is clicked
    if "editing_book_id" not in st.session_state:
        st.session_state["editing_book_id"] = None

    if select:
        book = select

        col1, col2 = st.columns(2)
        if col1.button("Edit Book"):
            st.session_state["editing_book_id"] = book.item_id

        if col2.button("Delete Book"):
            LibraryEngine.delete_book(book.item_id)
            st.success("Book deleted.")
            st.experimental_rerun()

    # If an edit was requested, render the edit modal for that book
    if st.session_state.get("editing_book_id"):
        edit_id = st.session_state["editing_book_id"]
        edit_book = next((b for b in books if b.item_id == edit_id), None)
        if edit_book:
            edit_book_modal(edit_book)


# ---------------------- EDIT MODAL ----------------------
def edit_book_modal(book: Book):
    st.markdown("<div class='section-header'>Edit Book</div>", unsafe_allow_html=True)

    form_key = f"edit_book_form_{book.item_id}"
    with st.form(form_key):
        title = st.text_input("Title", value=book.title)
        author = st.text_input("Author", value=book.author)
        publisher = st.text_input("Publisher", value=book.publisher)
        year = st.number_input("Year", value=book.year, min_value=1900, max_value=2100)
        # Ensure the book's current category is available in the select options
        categories = ["Computer Science", "Electronics", "Mechanical", "Mathematics", "Electrical"]
        if book.category and book.category not in categories:
            categories.insert(0, book.category)
        category = st.selectbox("Category", categories, index=categories.index(book.category) if book.category in categories else 0)
        copies = st.number_input("Copies", min_value=1, value=book.copies)

        save = st.form_submit_button("Save Changes")

    if save:
        LibraryEngine.edit_book(
            book.item_id,
            title=title,
            author=author,
            publisher=publisher,
            year=int(year),
            category=category,
            copies=int(copies)
        )
        # clear editing state then rerun
        try:
            st.session_state["editing_book_id"] = None
        except Exception:
            pass
        st.success("Book updated.")
        st.experimental_rerun()


# ---------------------- ADD BOOK ----------------------
def add_book_page():
    st.markdown("<div class='section-header'>Add New Book</div>", unsafe_allow_html=True)

    with st.form("add_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        publisher = st.text_input("Publisher")
        year = st.number_input("Year", min_value=1900, max_value=2100, value=2023)
        category = st.selectbox("Category", ["Computer Science", "Electronics", "Mechanical", "Mathematics", "Electrical"])
        copies = st.number_input("Copies", min_value=1, value=1)

        done = st.form_submit_button("Add Book")

    if done:
        new = Book(
            title=title or "Untitled",
            author=author or "Unknown",
            publisher=publisher or "Unknown",
            year=int(year),
            category=category,
            copies=int(copies)
        )
        books = LibraryEngine.list_books()
        books.append(new)
        LibraryEngine.save_books(books)
        st.success(f"Book added successfully (ID: {short_id(new.item_id)})")
        st.experimental_rerun()


# ---------------------- USERS PAGE ----------------------
def users_page():
    st.markdown("<div class='section-header'>Users</div>", unsafe_allow_html=True)
    
    users = LibraryEngine.list_users()
    idmap = id_to_title_map()

    table_rows = []
    for u in users:
        borrowed_names = [short_id(b) for b in u.borrowed]

        reserved_names = []
        for r in getattr(u, "reserved", []):
            reserved_names.append(short_id(r))
        table_rows.append({
            "Name": u.name,
            "Roll No": u.roll_no,
            "Email": u.email,
            "Borrowed (IDs)": ", ".join(borrowed_names),
            "Reserved (IDs)": ", ".join(reserved_names),
        })

    df = pd.DataFrame(table_rows)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Export Users CSV",
        convert_to_csv(table_rows),
        "users_export.csv"
    )
    # Unreserve section: allow removing a reservation from a user
    st.markdown("### Manage Reservations")

    if not users:
        st.info("No users available.")
    else:
        sel = st.selectbox("Select User to manage reservations", [f"{u.roll_no} - {u.name}" for u in users])
        roll = sel.split(" - ")[0]
        user = next(u for u in users if u.roll_no == roll)

        reserved_list = [f"{short_id(r)} — {r}" for r in getattr(user, "reserved", [])]
        if reserved_list:
            choice = st.selectbox("Reserved Items", reserved_list)
            res_id = choice.split(" — ")[1]
            if st.button("Unreserve"):
                LibraryEngine.unreserve_book(res_id, roll)
                st.success("Reservation removed.")
                st.experimental_rerun()
        else:
            st.info("This user has no reservations.")

    # Return Book section
    st.markdown("### Return Book")
    if not users:
        st.info("No users available.")
    else:
        sel_ret = st.selectbox("Select User to return a book", [f"{u.roll_no} - {u.name}" for u in users], key="ret_user")
        roll_ret = sel_ret.split(" - ")[0]
        user_ret = next(u for u in users if u.roll_no == roll_ret)

        borrow_list = [f"{short_id(book_id)} — {book_id}" for book_id in user_ret.borrowed]
        if borrow_list:
            choice_ret = st.selectbox("Borrowed Books", borrow_list, key="ret_borrowed")
            book_id_ret = choice_ret.split(" — ")[1]
            if st.button("Return Book", key="return_btn"):
                LibraryEngine.return_book(book_id_ret, roll_ret)
                st.success("Book returned successfully.")
                st.experimental_rerun()
        else:
            st.info("This user has no borrowed books.")


# ---------------------- ISSUE BOOK ----------------------
def issue_page():
    st.markdown("<div class='section-header'>Issue Book</div>", unsafe_allow_html=True)

    users = LibraryEngine.list_users()
    books = LibraryEngine.list_books()

    if not users or not books:
        st.info("No users or books available.")
        return

    user_choice = st.selectbox("Select User", [f"{u.roll_no} - {u.name}" for u in users])
    book_choice = st.selectbox("Select Book", [f"{short_id(b.item_id)} - {b.title}" for b in books])

    if st.button("Issue"):
        roll = user_choice.split(" - ")[0]
        # book_choice contains the short id; map it back to the full item_id
        short = book_choice.split(" - ")[0]
        book_obj = next((b for b in books if short_id(b.item_id) == short), None)
        if not book_obj:
            st.error("Selected book could not be resolved. Try again.")
        else:
            LibraryEngine.issue_book(book_obj.item_id, roll)
            st.success("Book issued successfully.")


# ---------------------- RESERVE PAGE ----------------------
def reserve_page():
    st.markdown("<div class='section-header'>Reserve Book</div>", unsafe_allow_html=True)
    users = LibraryEngine.list_users()
    books = LibraryEngine.list_books()

    u = st.selectbox("Select User", [f"{u.roll_no} - {u.name}" for u in users])
    b = st.selectbox("Select Book", [f"{short_id(b.item_id)} - {b.title}" for b in books])

    if st.button("Reserve"):
        roll = u.split(" - ")[0]
        short = b.split(" - ")[0]
        book_obj = next((bk for bk in books if short_id(bk.item_id) == short), None)
        if not book_obj:
            st.error("Selected book could not be resolved. Try again.")
        else:
            LibraryEngine.reserve_book(book_obj.item_id, roll)
            st.success("Book reserved.")


# ---------------------- CSV Export Helper ----------------------
def convert_to_csv(data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode("utf-8")
