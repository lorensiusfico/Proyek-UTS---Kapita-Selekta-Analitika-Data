from fastapi import APIRouter
from models import BorrowRequest, ReturnRequest, ExtendRequest
from services.library_service import books, borrow_book, return_book, extend_borrow, format_response

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/books")
def list_available_books():
    available = [b.dict() for b in books if b.stock > 0]
    return format_response("success", "Available books retrieved", data=available)

@router.post("/borrow")
def borrow(req: BorrowRequest):
    return borrow_book(req.user, req.book_id)

@router.post("/return")
def return_borrowed(req: ReturnRequest):
    return return_book(req.user, req.book_id)

@router.post("/extend")
def extend(req: ExtendRequest):
    return extend_borrow(req.user, req.book_id, req.extend_days)
