# main.py
from fastapi import FastAPI
from modules.library.routes import books, loans, reports

app = FastAPI(
    title="Sistem Peminjaman Buku Perpustakaan",
    description="API untuk mengelola buku dan peminjaman di perpustakaan universitas."
)

# Termasuk Router
app.include_router(books.router)
app.include_router(loans.router)
app.include_router(reports.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Selamat datang di API Perpustakaan! Kunjungi /docs untuk Swagger UI."}

# --- Catatan Penting ---
# Untuk menjalankan aplikasi FastAPI, Anda *harus* menggunakan server ASGI seperti Uvicorn.
# Anda melarang 'uvicorn', tetapi inilah cara server dijalankan dalam praktik:
# if __name__ == "__main__":
#     import uvicorn    
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)