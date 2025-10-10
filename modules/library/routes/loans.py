from fastapi import APIRouter, HTTPException
from datetime import date, timedelta
from typing import List
from modules.library.schema.schemas import Loan, Book

router = APIRouter()

# Simulasi data
books_db: List[Book] = [
    Book(id=1, title="Python for Data Science", author="Jake VanderPlas", stock=3),
    Book(id=2, title="Deep Learning", author="Ian Goodfellow", stock=2)
]
loans_db: List[Loan] = []

MAX_LOAN_DAYS = 30
DAILY_FINE = 2000  # denda per hari

# POST: pinjam buku
@router.post("/borrow", response_model=Loan)
def borrow_book(loan: Loan):
    for book in books_db:
        if book.id == loan.book_id:
            if book.stock <= 0:
                raise HTTPException(status_code=400, detail="Book out of stock")

            # kurangi stok dan buat catatan peminjaman
            book.stock -= 1
            loan.start_date = date.today()
            loan.due_date = date.today() + timedelta(days=7)
            loan.returned = False
            loans_db.append(loan)
            return loan

    raise HTTPException(status_code=404, detail="Book not found")

# PUT: perpanjang peminjaman
@router.put("/extend/{loan_id}", response_model=Loan)
def extend_loan(loan_id: int):
    for loan in loans_db:
        if loan.id == loan_id:
            total_days = (loan.due_date - loan.start_date).days
            if total_days >= MAX_LOAN_DAYS:
                raise HTTPException(status_code=400, detail="Cannot extend beyond 30 days")
            loan.due_date += timedelta(days=7)
            return loan
    raise HTTPException(status_code=404, detail="Loan not found")

# PUT: kembalikan buku
@router.put("/return/{loan_id}")
def return_book(loan_id: int):
    for loan in loans_db:
        if loan.id == loan_id:
            if loan.returned:
                raise HTTPException(status_code=400, detail="Book already returned")
            loan.returned = True
            delay_days = (date.today() - loan.due_date).days
            loan.late_days = max(0, delay_days)
            loan.fine = loan.late_days * DAILY_FINE

            # kembalikan stok buku
            for book in books_db:
                if book.id == loan.book_id:
                    book.stock += 1
                    break
            return {"message": "Book returned successfully", "fine": loan.fine}

    raise HTTPException(status_code=404, detail="Loan not found")