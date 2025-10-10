import sys
import os

# Menambahkan path ke folder modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

from fastapi import FastAPI
from modules.library.routes import books, loans, reports

app = FastAPI(
    title=" Sistem Manajemen Perpustakaan ",
    description=" Project 2: Library Management",
    version="1.0.0")

# Menambahkan router

app.include_router(books.router, prefix="/admin", tags=["Admin"])
app.include_router(loans.router, prefix="/student", tags=["Student"])
app.include_router(reports.router, prefix="/admin", tags=["Admin"])

@app.get("/")
def read_root():
    return {"message": "Selamat datang di sistem manajemen perpustakaan!"}

@app.get("/")
def root():
    """
    Endpoint.
    """
    return {"message": "Daftar peminjaman buku perpustakaan"}