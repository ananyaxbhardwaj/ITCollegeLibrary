# core/models.py
from dataclasses import dataclass, field
import random
from typing import List

# Generates a 15–16 digit numeric ID
def generate_numeric_id():
    return str(random.randint(10**14, 10**16 - 1))

@dataclass
class LibraryItem:
    item_id: str = field(default_factory=generate_numeric_id)

@dataclass
class Book(LibraryItem):
    title: str = ""
    author: str = ""
    publisher: str = ""
    year: int = 2023
    category: str = "General"
    copies: int = 1

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "year": self.year,
            "category": self.category,
            "copies": self.copies
        }

    @staticmethod
    def from_dict(d):
        return Book(
            item_id=d.get("item_id", generate_numeric_id()),
            title=d.get("title", ""),
            author=d.get("author", ""),
            publisher=d.get("publisher", ""),
            year=d.get("year", 2023),
            category=d.get("category", "General"),
            copies=d.get("copies", 1)
        )


@dataclass
class User:
    name: str = ""
    email: str = ""
    roll_no: str = ""
    contact: str = ""
    borrowed: List[str] = field(default_factory=list)
    reserved: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "roll_no": self.roll_no,
            "contact": self.contact,
            "borrowed": self.borrowed,
            "reserved": self.reserved
        }

    @staticmethod
    def from_dict(d):
        return User(
            name=d.get("name", ""),
            email=d.get("email", ""),
            roll_no=d.get("roll_no", ""),
            contact=d.get("contact", ""),
            borrowed=d.get("borrowed", []),
            reserved=d.get("reserved", [])
        )
