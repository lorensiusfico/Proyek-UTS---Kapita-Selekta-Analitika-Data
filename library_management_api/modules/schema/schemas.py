from pydantic import BaseModel, Field
from datetime import date

class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    stock: int = Field(ge=0)

class Book(BaseModel):
    book_id: str
    title: str
    author: str
    year: int
    stock: int

class LoanCreate(BaseModel):
    book_id: str
    days: int = Field(ge=1, le=14)  # pinjam awal max 14 hari

class Loan(BaseModel):
    loan_id: str
    book_id: str
    user_id: str
    start_date: date
    due_date: date
    total_days_allowed: int  # akumulasi izin hari (<=30)
    returned_date: date | None = None
    fine: int = 0
