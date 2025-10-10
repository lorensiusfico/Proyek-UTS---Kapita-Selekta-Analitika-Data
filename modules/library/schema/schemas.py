from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional

# --- Enum/Konstanta ---
MAX_LOAN_DAYS = 3  # Durasi pinjam awal (misalnya 14 hari)
MAX_TOTAL_LOAN_DAYS = 30  # Durasi pinjam total maksimum (termasuk perpanjangan)
DAILY_FINE_RATE = 1000  # Denda per hari (misalnya Rp 1000)

# --- Models ---
class BookBase(BaseModel):
    """Skema dasar untuk Buku."""
    title: str
    author: str
    isbn: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Atomic Habits",
                "author": "James Clear",
                "isbn": "978-0735211292"
            }
        }
    )


class BookCreate(BookBase):
    """Skema untuk membuat Buku baru (termasuk stok awal)."""
    stock: int = Field(..., gt=0)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Atomic Habits",
                "author": "James Clear",
                "isbn": "978-0735211292",
                "stock": 5
            }
        }
    )


class Book(BookCreate):
    """Skema Buku lengkap (termasuk ID dan stok yang dapat berubah)."""
    book_id: int
    available_stock: int

    model_config = ConfigDict(from_attributes=True)


class LoanBase(BaseModel):
    """Skema dasar untuk Peminjaman."""
    book_id: int
    student_id: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "book_id": 1,
                "student_id": "NIM12345"
            }
        }
    )


class LoanCreate(LoanBase):
    """Skema untuk membuat Peminjaman baru."""
    pass


class Loan(LoanCreate):
    """Skema Peminjaman lengkap (termasuk detail tanggal, status, dan denda)."""
    loan_id: int
    loan_date: date
    due_date: date
    return_date: Optional[date] = None
    is_active: bool = True
    delay_days: int = 0
    fine_amount: int = 0

    model_config = ConfigDict(from_attributes=True)


class LoanExtension(BaseModel):
    """Skema untuk perpanjangan pinjaman."""
    loan_id: int

    model_config = ConfigDict(
        json_schema_extra={"example": {"loan_id": 101}}
    )


class ReportLoan(Loan):
    """Skema Pinjaman untuk Laporan, mencakup detail buku."""
    book_title: str
    is_overdue: bool

    model_config = ConfigDict(from_attributes=True)
