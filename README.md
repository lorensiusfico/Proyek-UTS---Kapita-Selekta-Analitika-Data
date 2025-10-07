# Proyek-UTS---Kapita-Selekta-Analitika-Data
Repository untuk Proyek UTS: Library Management dari Kelompok 3

from fastapi import FastAPI
from modules.books.routes import router as books_router
from modules.loans.routes import router as loans_router

app = FastAPI()

# Include routes for books and loans
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(loans_router, prefix="/loans", tags=["loans"])
