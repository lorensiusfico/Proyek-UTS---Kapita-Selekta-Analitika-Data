# modules/routes/loans.py
from fastapi import APIRouter, status
from typing import List

from modules.library.schema.schemas import LoanCreate, Loan, LoanExtension
from modules.library.storage import repository
from modules.library.services import services

router = APIRouter(prefix="/loans", tags=["Mahasiswa: Peminjaman & Pengembalian"])

# --- Mahasiswa Activity ---

@router.post("/borrow", response_model=Loan, status_code=status.HTTP_201_CREATED)
def borrow_book(loan_data: LoanCreate):
    """Melakukan peminjaman buku oleh Mahasiswa."""
    return services.create_loan_service(loan_data)

@router.put("/extend", response_model=Loan)
def extend_loan(extension_data: LoanExtension):
    """Memperpanjang masa pinjam buku (dengan batasan total 30 hari)."""
    return services.extend_loan_service(extension_data.loan_id)

@router.put("/return/{loan_id}", response_model=Loan)
def return_book(loan_id: int):
    """Mengembalikan buku dan menghitung denda (jika ada)."""
    return services.return_loan_service(loan_id)

@router.get("/", response_model=List[Loan])
def get_all_loans():
    """Melihat daftar seluruh pinjaman (Admin/Debugging)."""
    loans = repository.get_all_loans()
    return [Loan.model_validate(l) for l in loans]

# Endpoint untuk Mahasiswa (opsional: melihat pinjaman sendiri)
@router.get("/my/{student_id}", response_model=List[Loan])
def get_student_loans(student_id: str):
    """Melihat daftar pinjaman aktif dan riwayat oleh Mahasiswa tertentu."""
    loans = [Loan.model_validate(l) for l in repository.get_all_loans() if l['student_id'] == student_id]
    return loans