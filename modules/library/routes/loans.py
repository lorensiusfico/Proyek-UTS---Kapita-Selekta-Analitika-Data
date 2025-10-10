from fastapi import APIRouter, HTTPException
from typing import List
from library.schema.schemas import Loan
from library.services.services import calculate_fine
from library.storage.repository import borrow_book, return_book, get_loans

router = APIRouter()

@router.post("/borrow")
def borrow(loan: Loan):
    return borrow_book(loan)


@router.get("/loans", response_model=List[Loan])
def list_loans():
    return get_loans()  # Mengambil data peminjaman

@router.post("/return")
def return_book(loan: Loan):
    fine = calculate_fine(loan.book_id, loan.borrow_date, loan.return_date)
    return_book(loan, fine)
    return {"message": "Buku dikembalikan", "fine": fine}


