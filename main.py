from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers dari modul
from modules.library.routes import books, loans, reports

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Library Management API",
    description=(
        "API sistem manajemen perpustakaan untuk tugas Kapita Selekta Analitika Data.\n\n"
        "Fitur utama:\n"
        "- Admin: CRUD buku\n"
        "- Mahasiswa: Pinjam, Kembali, Perpanjang Buku\n"
        "- Laporan: Daftar pinjaman aktif & keterlambatan\n"
    ),
    version="1.0.0",
)

# Middleware (opsional, agar API bisa diakses dari frontend / Postman)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrasi router
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(loans.router, prefix="/loans", tags=["Loans"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

# Endpoint utama (root)
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Library Management API 🚀",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }

# Jalankan server (untuk testing lokal)
# Simpan file ini sebagai main.py lalu jalankan dengan:
# uvicorn main:app --reload