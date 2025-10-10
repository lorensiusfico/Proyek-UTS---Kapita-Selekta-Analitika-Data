from pydantic import BaseModel
from datetime import date
from typing import Optional

# --- Model Buku ---
class Book(BaseModel):
    id: int
    title: str
    author: str
    stock: int

# --- Model Mahasiswa (opsional, bisa dikembangkan nanti) ---
class User(BaseModel):
    id: int
    name: str
    email: str

# --- Model Peminjaman Buku ---
class Loan(BaseModel):
    id: int
    book_id: int
    user_id: int
    start_date: Optional[date] = None