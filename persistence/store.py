# persistence/store.py
import json
from pathlib import Path
from core.models import Book, User

DATA_DIR = Path("data")
BOOKS_FILE = DATA_DIR / "books.json"
USERS_FILE = DATA_DIR / "users.json"
LOANS_FILE = DATA_DIR / "loans.json"


# ---------------- Utility functions ----------------
def _ensure_data_folder():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)


def _read(path):
    _ensure_data_folder()
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _write(path, data):
    _ensure_data_folder()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ---------------- Data Store Layer ----------------

class DataStore:

    # ---- BOOKS ----
    @staticmethod
    def load_books():
        raw = _read(BOOKS_FILE)
        return [Book.from_dict(item) for item in raw]

    @staticmethod
    def save_books(books):
        _write(BOOKS_FILE, [b.to_dict() for b in books])

    # ---- USERS ----
    @staticmethod
    def load_users():
        raw = _read(USERS_FILE)
        return [User.from_dict(item) for item in raw]

    @staticmethod
    def save_users(users):
        _write(USERS_FILE, [u.to_dict() for u in users])

    # ---- LOANS ----
    @staticmethod
    def load_loans():
        # Loans feature removed: keep existing file untouched but do not load loans
        # Return an empty list so the rest of the app stops relying on loans data.
        return []

    @staticmethod
    def save_loans(loans):
        # Loans feature removed: no-op save to avoid creating/updating loans.json
        return
