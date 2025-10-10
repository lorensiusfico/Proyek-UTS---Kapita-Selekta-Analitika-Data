from datetime import datetime
from typing import List
from library.schema.schemas import Book, Loan, Report

# Data buku yang diperoleh dari gambar yang Anda upload, dengan nama 'daftarbuku'
daftarbuku = [
    Book(id=1, title="The Adventures of Chronicles", author="Jordan Brown", category="Programming", stock=4),
    Book(id=2, title="The Dream of Shadows", author="Taylor Walker", category="History", stock=3),
    Book(id=3, title="The Shadows of Mystery", author="Jordan Johnson", category="Science", stock=5),
    Book(id=4, title="The Chronicles of Dream", author="Casey Walker", category="Fiction", stock=4),
    Book(id=5, title="The Future of Adventures", author="Skyler Lee", category="Programming", stock=3),
    Book(id=6, title="The Chronicles of Chronicles", author="Skyler Smith", category="Thriller", stock=4),
    Book(id=7, title="The Journey of Adventures", author="Morgan Hall", category="Fiction", stock=2),
    Book(id=8, title="The Legacy of Quest", author="Alex Clark", category="Science", stock=3),
    Book(id=9, title="The Mystery of Dream", author="Jordan Anderson", category="Fiction", stock=1),
    Book(id=10, title="The Adventures of Shadows", author="Dakota Taylor", category="Programming", stock=5),
]

 # Data peminjaman
loans_db = [
    Loan(user_id=1, book_id=2, borrow_date="2025-09-01", return_date="2025-09-15", fine=0),
    Loan(user_id=2, book_id=5, borrow_date="2025-09-05", return_date="2025-09-20", fine=1000),
]
 # Data Laporan
reports_db = [
    Report(user_id=1, borrowed_books=[1, 2], overdue_books=[3], total_fine=1000),
    Report(user_id=2, borrowed_books=[3], overdue_books=[], total_fine=0),
]

# Fungsi untuk mengambil data peminjaman
def get_loans() -> List[Loan]:
    return loans_db  # Mengembalikan data peminjaman

def generate_report() -> List[Report]:
    return reports_db  # Mengembalikan data laporan
    
def get_books() -> List[Book]:
    return daftarbuku

def add_book(book: Book) -> Book:
    daftarbuku.append(book)
    return book

def update_book(book_id: int, updated_book: Book) -> Book:
    for book in daftarbuku:
        if book.id == book_id:
            book.title = updated_book.title
            book.author = updated_book.author
            book.category = updated_book.category
            book.stock = updated_book.stock
            return book
    raise HTTPException(status_code=404, detail="Buku tidak ditemukan")

def delete_book(book_id: int) -> dict:
    global daftarbuku
    daftarbuku = [book for book in daftarbuku if book.id != book_id]
    return {"message": "Buku berhasil dihapus"}
    
# Fungsi untuk meminjam buku
def borrow_book(user_id: int, book_id: int, borrow_date: datetime, return_date: datetime):
    # Logika untuk menyimpan data peminjaman
    return {"message": "Buku berhasil dipinjam", "user_id": user_id, "book_id": book_id}

# Fungsi untuk mengembalikan buku
def return_book(user_id: int, book_id: int, return_date: datetime):
    # Logika untuk mengembalikan buku
    return {"message": "Buku berhasil dikembalikan", "user_id": user_id, "book_id": book_id}