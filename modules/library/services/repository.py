import csv
from typing import List
from modules.library.schema.schemas import Book

BOOKS_FILE = "data_books.csv"

# Simpan daftar buku ke CSV
def save_books_to_csv(books: List[Book]):
    with open(BOOKS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=Book.model_fields.keys())
        writer.writeheader()
        for book in books:
            writer.writerow(book.dict())

# Baca daftar buku dari CSV
def load_books_from_csv() -> List[Book]:
    books = []
    try:
        with open(BOOKS_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                books.append(Book(**row))
    except FileNotFoundError:
        pass
    return books