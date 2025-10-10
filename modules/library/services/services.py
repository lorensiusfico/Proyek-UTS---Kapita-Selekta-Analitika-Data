from datetime import datetime, timedelta
from library.schema.schemas import Loan, Book
from library.storage.repository import get_books

# Fungsi untuk menghitung denda berdasarkan tanggal jatuh tempo
def calculate_fine(book_id: int, borrow_date: datetime, return_date: datetime) -> float:
    due_date = borrow_date + timedelta(days=30)  # Mengasumsikan batas pinjam adalah 30 hari
    if return_date > due_date:
        days_late = (return_date - due_date).days
        return days_late * 1000  # Misalkan denda 1000 per hari keterlambatan
    return 0

# Membuat laporan untuk admin
def generate_report(user_id: int):
    # Implementasi untuk laporan buku terlambat
    overdue_books = []  # Tempat penyimpanan untuk logika buku terlambat
    total_fine = 0
    # Mengembalikan objek laporan (ini bisa diperluas sesuai dengan data Anda)
    return {"user_id": user_id, "overdue_books": overdue_books, "total_fine": total_fine}
