from fastapi import APIRouter
from models import Book
from services.library_service import books, add_book, format_response

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/books")
def add_new_book(book: Book):
    return add_book(book)

@router.get("/books")
def list_all_books():
    return format_response("success", "All books retrieved", data=[b.dict() for b in books])

@router.get("/borrowed")
def borrowed_books():
    borrowed = [t for t in books if t.stock == 0]
    return format_response("success", "Borrowed books retrieved", data=borrowed)
