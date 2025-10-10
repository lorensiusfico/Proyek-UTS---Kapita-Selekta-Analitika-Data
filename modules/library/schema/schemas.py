from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Book(BaseModel):
    id: int
    title: str
    author: str
    stock: int
    category: str
class Loan(BaseModel):
    user_id: int
    book_id: int
    borrow_date: datetime
    return_date: datetime
    fine: Optional[float] = 0

class User(BaseModel):
    user_id: int
    username: str
    role: str  # admin/mahasiswa

class Report(BaseModel):
    user_id: int
    borrowed_books: List[Book]
    overdue_books: List[Book]
    total_fine: float


class Report(BaseModel):
    user_id: int
    borrowed_books: List[int]  # Daftar ID buku yang dipinjam
    overdue_books: List[int]   # Daftar ID buku yang terlambat
    total_fine: float     