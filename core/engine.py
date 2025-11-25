# core/engine.py
from persistence.store import DataStore
from core.models import Book, User
from typing import List, Dict
from datetime import date, timedelta, datetime

FINE_PER_DAY = 10.0  # currency units per day overdue

class LibraryEngine:

    # --- Basic wrappers (books/users/loans) ---
    @staticmethod
    def list_books() -> List[Book]:
        return DataStore.load_books()

    @staticmethod
    def save_books(books: List[Book]):
        DataStore.save_books(books)

    @staticmethod
    def list_users() -> List[User]:
        return DataStore.load_users()

    @staticmethod
    def save_users(users: List[User]):
        DataStore.save_users(users)

    @staticmethod
    def list_loans() -> List[Dict]:
        # Loans feature removed: always return empty list
        return []

    @staticmethod
    def save_loans(loans: List[Dict]):
        # Loans feature removed: no-op
        return

    # --- Issue a book (adds book_id to user's borrowed and create loan) ---
    @staticmethod
    def issue_book(book_id: str, user_roll: str, period_days: int = 14):
        # Issue book: only update user's borrowed list (no loan records)
        users = LibraryEngine.list_users()
        for u in users:
            if u.roll_no == user_roll:
                if book_id not in getattr(u, "borrowed", []):
                    u.borrowed.append(book_id)
        LibraryEngine.save_users(users)

    # --- Reserve a book (create a reservation entry in loans with reserved=True) ---
    @staticmethod
    def reserve_book(book_id: str, user_roll: str):
        # Add reservation to the user's reserved list
        users = LibraryEngine.list_users()
        for u in users:
            if u.roll_no == user_roll:
                if book_id not in getattr(u, "reserved", []):
                    u.reserved.append(book_id)
        LibraryEngine.save_users(users)

    @staticmethod
    def unreserve_book(book_id: str, user_roll: str):
        # Remove reservation from user's reserved list
        users = LibraryEngine.list_users()
        for u in users:
            if u.roll_no == user_roll:
                if book_id in getattr(u, "reserved", []):
                    u.reserved.remove(book_id)
        LibraryEngine.save_users(users)

    @staticmethod
    def return_book(book_id: str, user_roll: str):
        """Return a book by removing it from the user's borrowed list."""
        users = LibraryEngine.list_users()
        for u in users:
            if u.roll_no == user_roll:
                if book_id in getattr(u, "borrowed", []):
                    u.borrowed.remove(book_id)
        LibraryEngine.save_users(users)
        return True

    # Return book feature removed. To return a book, remove it from the user's
    # `borrowed` list directly via `LibraryEngine.save_users` after modifying the user.

    # --- Delete a book by item_id ---
    @staticmethod
    def delete_book(book_id: str):
        books = LibraryEngine.list_books()
        books = [b for b in books if b.item_id != book_id]
        LibraryEngine.save_books(books)

        # remove from users borrowed lists
        users = LibraryEngine.list_users()
        changed = False
        for u in users:
            if book_id in getattr(u, "borrowed", []):
                u.borrowed.remove(book_id)
                changed = True
        if changed:
            LibraryEngine.save_users(users)

        # remove related loans/reservations
        loans = LibraryEngine.list_loans() or []
        loans = [l for l in loans if l.get("item_id") != book_id]
        LibraryEngine.save_loans(loans)

    # --- Edit book (update allowed fields) ---
    @staticmethod
    def edit_book(book_id: str, **fields):
        books = LibraryEngine.list_books()
        for b in books:
            if b.item_id == book_id:
                for k, v in fields.items():
                    if hasattr(b, k):
                        # Cast numeric fields to int if appropriate
                        if k in ("year", "copies"):
                            try:
                                v = int(v)
                            except Exception:
                                # keep original if cast fails
                                pass
                        setattr(b, k, v)
                break
        LibraryEngine.save_books(books)
        return True

    # --- Counts summary for dashboard ---
    @staticmethod
    def counts():
        books = LibraryEngine.list_books()
        users = LibraryEngine.list_users()
        total_copies = sum([b.copies for b in books])
        unique_titles = len(books)
        total_users = len(users)
        # active_loans is derived from users' borrowed lists now
        active_loans = sum(len(getattr(u, "borrowed", [])) for u in users)
        reservations = sum(len(getattr(u, "reserved", [])) for u in users)
        overdue_count = 0
        return {
            "total_titles": unique_titles,
            "total_copies": total_copies,
            "total_users": total_users,
            "active_loans": active_loans,
            "reservations": reservations,
            "overdue_count": overdue_count
        }

    # --- Overdue detection + fine calculation ---
    @staticmethod
    def _parse_date(s: str):
        # expects 'YYYY-MM-DD' as produced by str(date.today())
        try:
            return datetime.fromisoformat(s).date()
        except Exception:
            try:
                return datetime.strptime(s, "%Y-%m-%d").date()
            except Exception:
                return None

    @staticmethod
    def get_overdue_loans(fine_per_day: float = FINE_PER_DAY):
        """
        Returns a list of dicts with:
        { item_id, user_roll, loan_date, due_date, days_overdue, fine_amount }
        Only returns loans that are not returned and not reservations and due_date < today.
        """
        # Overdue detection removed with loans feature. Return empty list.
        return []

    @staticmethod
    def total_fines_for_user(user_roll: str, fine_per_day: float = FINE_PER_DAY):
        # Fine calculation removed with loans feature.
        return 0.0
