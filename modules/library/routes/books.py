from fastapi import APIRouter, HTTPException
from typing import List
from modules.library.schema.schemas import Book

router = APIRouter()

# Simulasi data buku (sementara disimpan di memori)
books_db = [
    Book(id=1, title="Python for Data Science", author="Jake VanderPlas", stock=3),
    Book(id=2, title="Deep Learning", author="Ian Goodfellow", stock=2)
]

# GET: lihat semua buku
@router.get("/", response_model=List[Book])
def get_all_books():
    return books_db

# GET: cari buku berdasarkan ID
@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# POST: tambah buku baru
@router.post("/", response_model=Book)
def add_book(book: Book):
    if any(b.id == book.id for b in books_db):
        raise HTTPException(status_code=400, detail="Book ID already exists")
    books_db.append(book)
    return book

# PUT: update buku
@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            books_db[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# DELETE: hapus buku
@router.delete("/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[i]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")