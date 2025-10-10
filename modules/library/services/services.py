# modules/services/services.py
from datetime import date, timedelta, datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status

from modules.library.storage import repository
from modules.library.schema.schemas import (
    BookCreate, Book, LoanCreate, Loan,
    MAX_LOAN_DAYS, MAX_TOTAL_LOAN_DAYS, DAILY_FINE_RATE
)

# --- Book/Stock Services (Admin) ---

def create_new_book_service(book_data: BookCreate) -> Book:
    """Tambahkan buku baru dan inisialisasi stok."""
    book_dict = book_data.model_dump()
    new_book_dict = repository.create_book(book_dict)
    return Book.model_validate(new_book_dict)

def update_book_stock(book_id: int, change: int) -> bool:
    """Perbarui available_stock buku (digunakan saat pinjam/kembali)."""
    book = repository.get_book_by_id(book_id)
    if not book:
        return False

    new_stock = book["available_stock"] + change

    # 🚨 Cegah stok negatif
    if new_stock < 0:
        return False

    # 🧠 Simpan stok baru dengan update_data lengkap
    update_data = {"available_stock": new_stock}
    repository.update_book(book_id, update_data)

    # 🧾 Pastikan sinkron juga ke objek lokal
    book["available_stock"] = new_stock
    return True

# --- Loan Services (Student) ---

def calculate_due_date(loan_date: date) -> date:
    """Hitung tanggal jatuh tempo (default 14 hari)."""
    return loan_date + timedelta(days=MAX_LOAN_DAYS)

def create_loan_service(loan_data: LoanCreate) -> Loan:
    """Proses peminjaman baru."""
    book_id = loan_data.book_id
    book = repository.get_book_by_id(book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buku tidak ditemukan."
        )

    # 🚨 Cek stok habis
    if book['available_stock'] <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Buku tidak ditemukan atau stok kosong."
        )


    # 🔥 Kurangi stok
    if not update_book_stock(book_id, -1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Gagal memperbarui stok buku (kemungkinan stok habis)."
        )

    loan_date = date.today()
    due_date = calculate_due_date(loan_date)

    loan_dict = {
        **loan_data.model_dump(),
        "loan_date": loan_date,
        "due_date": due_date,
        "is_active": True,
        "delay_days": 0,
        "fine_amount": 0,
        "return_date": None
    }

    new_loan_dict = repository.create_loan(loan_dict)
    return Loan.model_validate(new_loan_dict)

def extend_loan_service(loan_id: int) -> Loan:
    """Proses perpanjangan peminjaman."""
    loan = repository.get_loan_by_id(loan_id)

    if not loan or not loan.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pinjaman tidak ditemukan atau sudah dikembalikan."
        )

    loan_date: date = loan["loan_date"]
    current_due_date: date = loan["due_date"]
    
    # Cek durasi total
    total_days_elapsed = (current_due_date - loan_date).days
    
    # Hanya boleh perpanjang jika total durasi tidak melebihi MAX_TOTAL_LOAN_DAYS
    # Perpanjangan standar: 14 hari lagi
    extension_days = MAX_LOAN_DAYS
    
    if total_days_elapsed + extension_days > MAX_TOTAL_LOAN_DAYS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Perpanjangan akan melebihi batas total {MAX_TOTAL_LOAN_DAYS} hari."
        )

    new_due_date = current_due_date + timedelta(days=extension_days)
    
    updated_loan_dict = repository.update_loan(loan_id, {"due_date": new_due_date})
    return Loan.model_validate(updated_loan_dict)

def calculate_fine(due_date, return_date: date) -> (int, int):
    """Hitung hari keterlambatan dan denda."""
    # Pastikan due_date bertipe date
    if isinstance(due_date, str):
        due_date = datetime.fromisoformat(due_date).date()

    if return_date <= due_date:
        return 0, 0

    delay_days = (return_date - due_date).days
    fine_amount = delay_days * DAILY_FINE_RATE
    return delay_days, fine_amount

def return_loan_service(loan_id: int) -> Loan:
    """Proses pengembalian buku."""
    loan = repository.get_loan_by_id(loan_id)

    if not loan or not loan.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pinjaman tidak ditemukan atau sudah dikembalikan."
        )

    return_date = date.today()
    due_date: date = loan["due_date"]

    delay_days, fine_amount = calculate_fine(due_date, return_date)

    update_data = {
        "is_active": False,
        "return_date": return_date,
        "delay_days": delay_days,
        "fine_amount": fine_amount
    }
    
    # Tambah stok buku
    if not update_book_stock(loan["book_id"], 1):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gagal memperbarui stok buku saat pengembalian."
        )

    updated_loan_dict = repository.update_loan(loan_id, update_data)
    return Loan.model_validate(updated_loan_dict)

# --- Report Services (Admin) ---

def get_active_and_overdue_loans_report() -> List[Dict[str, Any]]:
    """Dapatkan daftar pinjaman aktif, tandai yang overdue, dan gabungkan dengan detail buku."""
    active_loans = repository.get_active_loans()
    report_list = []
    today = date.today()

    for loan in active_loans:
        book = repository.get_book_by_id(loan["book_id"])
        
        is_overdue = loan["due_date"] < today
        
        report_data = {
            **loan,
            "book_title": book["title"] if book else "Buku Tidak Ditemukan",
            "is_overdue": is_overdue
        }
        report_list.append(report_data)
        
    return report_list