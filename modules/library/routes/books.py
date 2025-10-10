from fastapi import APIRouter, HTTPException
from typing import List
from library.schema.schemas import Book
from library.storage.repository import get_books, add_book, update_book, delete_book

router = APIRouter()

@router.get("/books", response_model=List[Book])
def list_books():
    return get_books()

@router.post("/books", response_model=Book)
def create_book(book: Book):
    return add_book(book)

@router.put("/books/{book_id}", response_model=Book)
def modify_book(book_id: int, book: Book):
    return update_book(book_id, book)

@router.delete("/books/{book_id}")
def remove_book(book_id: int):
    return delete_book(book_id)

