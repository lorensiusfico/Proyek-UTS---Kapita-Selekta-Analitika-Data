from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class Book(BaseModel):
    id: int = Field(..., gt=0)
    title: str
    author: str
    stock: int = Field(..., ge=0)

class BorrowRequest(BaseModel):
    user: str
    book_id: int

class ReturnRequest(BaseModel):
    user: str
    book_id: int

class ExtendRequest(BaseModel):
    user: str
    book_id: int
    extend_days: int = Field(..., gt=0)

class Transaction(BaseModel):
    user: str
    book_id: int
    borrow_date: date
    due_date: date
    return_date: Optional[date] = None
    fine: int = 0

class UserRoleRequest(BaseModel):
    user: str
    role: str  # 'admin' atau 'student'
