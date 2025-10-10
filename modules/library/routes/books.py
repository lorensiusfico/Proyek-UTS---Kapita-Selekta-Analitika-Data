# modules/routes/books.py
from fastapi import APIRouter, HTTPException, status
from typing import List

from modules.library.schema.schemas import BookCreate, Book
from modules.library.storage import repository
from modules.library.services import services

router = APIRouter(prefix="/admin/books", tags=["Admin: Pengelolaan Buku"])

# --- CRUD Buku ---

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    """Menambahkan buku baru ke perpustakaan (Admin)."""
    return services.create_new_book_service(book)

@router.get("/", response_model=List[Book])
def read_books():
    """Mendapatkan daftar semua buku."""
    books = repository.get_all_books()
    return [Book.model_validate(b) for b in books]

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int):
    """Mendapatkan detail buku berdasarkan ID."""
    book = repository.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buku tidak ditemukan")
    return Book.model_validate(book)

@router.put("/{book_id}", response_model=Book)
def update_book_info(book_id: int, book_update: BookCreate):
    """Memperbarui informasi buku (Admin)."""
    updated_book = repository.update_book(book_id, book_update.model_dump())
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buku tidak ditemukan")
    return Book.model_validate(updated_book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_info(book_id: int):
    """Menghapus buku dari sistem (Admin)."""
    if not repository.delete_book(book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buku tidak ditemukan")
    return # No content

