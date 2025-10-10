from typing import List, Dict, Any, Optional
from datetime import date, timedelta
import random
import csv
import os

# ============================================
# 📚 DATA DUMMY (30 Buku + 2 Peminjaman)
# ============================================

# Daftar judul & penulis dummy
book_titles = [
    ("Atomic Habits", "James Clear"),
    ("Deep Work", "Cal Newport"),
    ("Clean Code", "Robert C. Martin"),
    ("The Pragmatic Programmer", "Andrew Hunt"),
    ("Refactoring", "Martin Fowler"),
    ("The Psychology of Money", "Morgan Housel"),
    ("Start With Why", "Simon Sinek"),
    ("Thinking, Fast and Slow", "Daniel Kahneman"),
    ("The 7 Habits of Highly Effective People", "Stephen R. Covey"),
    ("Outliers", "Malcolm Gladwell"),
    ("Grit", "Angela Duckworth"),
    ("Essentialism", "Greg McKeown"),
    ("So Good They Can't Ignore You", "Cal Newport"),
    ("Cracking the Coding Interview", "Gayle Laakmann McDowell"),
    ("Algorithms to Live By", "Brian Christian"),
    ("Zero to One", "Peter Thiel"),
    ("Lean Startup", "Eric Ries"),
    ("Hooked", "Nir Eyal"),
    ("Rework", "Jason Fried"),
    ("Drive", "Daniel H. Pink"),
    ("Mindset", "Carol S. Dweck"),
    ("Can't Hurt Me", "David Goggins"),
    ("Educated", "Tara Westover"),
    ("The Subtle Art of Not Giving a F*ck", "Mark Manson"),
    ("Ikigai", "Héctor García"),
    ("Digital Minimalism", "Cal Newport"),
    ("Extreme Ownership", "Jocko Willink"),
    ("The Power of Now", "Eckhart Tolle"),
    ("12 Rules for Life", "Jordan B. Peterson"),
    ("The Lean Product Playbook", "Dan Olsen"),
]

_BOOKS: Dict[int, Dict[str, Any]] = {}

for i, (title, author) in enumerate(book_titles, start=1):
    stock = random.randint(2, 10)
    _BOOKS[i] = {
        "book_id": i,
        "title": title,
        "author": author,
        "isbn": f"978-000000{i:03d}",
        "stock": stock,
        "available_stock": stock - random.randint(0, 2),  # sebagian sedang dipinjam
    }

# Contoh data peminjaman dummy
_LOANS: Dict[int, Dict[str, Any]] = {
    1: {
        "loan_id": 1,
        "book_id": 5,
        "student_id": "NIM1001",
        "loan_date": date.today() - timedelta(days=8),
        "due_date": date.today() + timedelta(days=6),
        "return_date": None,
        "is_active": True,
        "delay_days": 0,
        "fine_amount": 0,
    },
    2: {
        "loan_id": 2,
        "book_id": 2,
        "student_id": "NIM1002",
        "loan_date": date.today() - timedelta(days=20),
        "due_date": date.today() - timedelta(days=5),
        "return_date": None,
        "is_active": True,
        "delay_days": 5,
        "fine_amount": 5000,
    }
}

_NEXT_BOOK_ID = len(_BOOKS) + 1
_NEXT_LOAN_ID = len(_LOANS) + 1


# ============================================
# 💾 Fungsi untuk Simpan & Muat CSV
# ============================================

def save_books_to_csv():
    """Simpan data buku ke file CSV."""
    with open(BOOKS_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["book_id", "title", "author", "isbn", "stock", "available_stock"])
        writer.writeheader()
        for book in _BOOKS.values():
            writer.writerow(book)

def load_books_from_csv():
    """Muat data buku dari file CSV jika ada."""
    global _BOOKS, _NEXT_BOOK_ID
    if not os.path.exists(BOOKS_FILE):
        return
    with open(BOOKS_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            book_id = int(row["book_id"])
            _BOOKS[book_id] = {
                "book_id": book_id,
                "title": row["title"],
                "author": row["author"],
                "isbn": row["isbn"],
                "stock": int(row["stock"]),
                "available_stock": int(row["available_stock"]),
            }
    _NEXT_BOOK_ID = max(_BOOKS.keys()) + 1 if _BOOKS else 1


def save_loans_to_csv():
    """Simpan data peminjaman ke file CSV."""
    with open(LOANS_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "loan_id", "book_id", "student_id", "loan_date", "due_date",
            "return_date", "is_active", "delay_days", "fine_amount"
        ])
        writer.writeheader()
        for loan in _LOANS.values():
            # Konversi tanggal ke string biar bisa disimpan di CSV
            row = loan.copy()
            for k in ["loan_date", "due_date", "return_date"]:
                if isinstance(row[k], date):
                    row[k] = row[k].isoformat()
            writer.writerow(row)

def load_loans_from_csv():
    """Muat data peminjaman dari file CSV jika ada."""
    global _LOANS, _NEXT_LOAN_ID
    if not os.path.exists(LOANS_FILE):
        return
    with open(LOANS_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            loan_id = int(row["loan_id"])
            _LOANS[loan_id] = {
                "loan_id": loan_id,
                "book_id": int(row["book_id"]),
                "student_id": row["student_id"],
                "loan_date": date.fromisoformat(row["loan_date"]),
                "due_date": date.fromisoformat(row["due_date"]),
                "return_date": date.fromisoformat(row["return_date"]) if row["return_date"] else None,
                "is_active": row["is_active"].lower() == "true",
                "delay_days": int(row["delay_days"]),
                "fine_amount": int(row["fine_amount"]),
            }
    _NEXT_LOAN_ID = max(_LOANS.keys()) + 1 if _LOANS else 1


# ============================================
# 📘 Fungsi Repository
# ============================================

def reset_data():
    """Reset semua data (untuk testing)."""
    global _BOOKS, _LOANS, _NEXT_BOOK_ID, _NEXT_LOAN_ID
    _BOOKS = {}
    _LOANS = {}
    _NEXT_BOOK_ID = 1
    _NEXT_LOAN_ID = 1

def get_all_books() -> List[Dict[str, Any]]:
    return list(_BOOKS.values())

def get_book_by_id(book_id: int) -> Optional[Dict[str, Any]]:
    return _BOOKS.get(book_id)

def create_book(book_data: Dict[str, Any]) -> Dict[str, Any]:
    global _NEXT_BOOK_ID
    new_book = {
        "book_id": _NEXT_BOOK_ID,
        "available_stock": book_data["stock"],
        **book_data
    }
    _BOOKS[_NEXT_BOOK_ID] = new_book
    _NEXT_BOOK_ID += 1
    save_books_to_csv()  # <--- simpan otomatis
    return new_book

def update_book(book_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if book_id in _BOOKS:
        for key, value in update_data.items():
            if key in ["title", "author", "isbn", "stock"]:
                _BOOKS[book_id][key] = value
        _BOOKS[book_id]["available_stock"] = _BOOKS[book_id]["stock"]
        save_books_to_csv()  # <--- simpan otomatis
        return _BOOKS[book_id]
    return None

def delete_book(book_id: int) -> bool:
    if book_id in _BOOKS:
        del _BOOKS[book_id]
        save_books_to_csv()  # <--- simpan otomatis
        return True
    return False

def get_all_loans() -> List[Dict[str, Any]]:
    return list(_LOANS.values())

def get_loan_by_id(loan_id: int) -> Optional[Dict[str, Any]]:
    return _LOANS.get(loan_id)

def create_loan(loan_data: Dict[str, Any]) -> Dict[str, Any]:
    global _NEXT_LOAN_ID
    new_loan = {
        "loan_id": _NEXT_LOAN_ID,
        **loan_data
    }
    _LOANS[_NEXT_LOAN_ID] = new_loan
    _NEXT_LOAN_ID += 1
    return new_loan

def update_loan(loan_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if loan_id in _LOANS:
        _LOANS[loan_id].update(update_data)
        return _LOANS[loan_id]
    return None

def get_active_loans() -> List[Dict[str, Any]]:
    return [loan for loan in _LOANS.values() if loan.get("is_active")]


# ============================================
# 🚀 Muat data CSV (jalankan terakhir)
# ============================================

# Tentukan nama file CSV di sini
BOOKS_FILE = "books.csv"
LOANS_FILE = "loans.csv"

# Kalau file CSV sudah ada, otomatis muat datanya
load_books_from_csv()
load_loans_from_csv()
