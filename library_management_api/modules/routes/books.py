from fastapi import APIRouter, Header, HTTPException
from library_management_api.modules.schema.schemas import BookCreate, Book, Book as BookModel
from library_management_api.modules.storage.repository import BOOKS, new_book_id

router = APIRouter(prefix="/books", tags=["books"])

def require_admin(x_role: str):
    if x_role != "admin":
        raise HTTPException(403, "Admin only")

@router.get("", response_model=list[Book])
def list_books():
    return list(BOOKS.values())

@router.get("/available", response_model=list[Book])
def list_available():
    return [b for b in BOOKS.values() if b["stock"] > 0]

@router.post("", response_model=Book)
def create_book(data: BookCreate, x_role: str = Header(..., alias="X-Role")):
    require_admin(x_role)
    book_id = new_book_id()
    book = BookModel(book_id=book_id, **data.model_dump())
    BOOKS[book_id] = book.model_dump()
    return BOOKS[book_id]

@router.patch("/{book_id}", response_model=Book)
def update_book(book_id: str, data: BookCreate, x_role: str = Header(..., alias="X-Role")):
    require_admin(x_role)
    if book_id not in BOOKS:
        raise HTTPException(404, "Book not found")
    BOOKS[book_id].update(data.model_dump())
    return BOOKS[book_id]

@router.delete("/{book_id}")
def delete_book(book_id: str, x_role: str = Header(..., alias="X-Role")):
    require_admin(x_role)
    if book_id not in BOOKS:
        raise HTTPException(404, "Book not found")
    del BOOKS[book_id]
    return {"deleted": book_id}
