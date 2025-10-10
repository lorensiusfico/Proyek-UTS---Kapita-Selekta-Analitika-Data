import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# 1️⃣ Test peminjaman buku
def test_borrow_book():
    response = client.post("/loans/borrow", json={"user": "Alice", "book_id": 1})
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["data"]["book_id"] == 1

# 2️⃣ Test pengembalian tepat waktu (tanpa denda)
def test_return_no_fine():
    # Pinjam buku baru (id 2)
    client.post("/loans/borrow", json={"user": "Alice", "book_id": 2})

    # Kembalikan langsung tanpa simulasi keterlambatan
    response = client.post("/loans/return", json={"user": "Alice", "book_id": 2})
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["data"]["fine"] == 0

# 3️⃣ Test pengembalian terlambat
def test_return_with_fine_via_clock():
    # Set tanggal pinjam 2025-10-10 oleh admin
    client.post("/loans/debug/clock/set", json={
        "user": "Lorensius",
        "role": "admin",
        "date": "2025-10-10"
    })
    
    # Alice meminjam buku (tanggal 10 Okt)
    client.post("/loans/borrow", json={"user": "Alice", "book_id": 3})

    # Admin memajukan waktu 20 hari
    client.post("/loans/debug/clock/advance", json={
        "user": "Lorensius",
        "role": "admin",
        "days": 20
    })

    # Alice mengembalikan buku
    resp = client.post("/loans/return", json={"user": "Alice", "book_id": 3})
    data = resp.json()

    assert resp.status_code == 200
    assert data["data"]["fine"] == 6000  # 6 hari * 1000 per hari

    # Bersihkan clock override
    client.post("/loans/debug/clock/clear", json={
        "user": "Lorensius",
        "role": "admin"
    })


# 4️⃣ Test admin bisa akses laporan
def test_admin_reports_access():
    response = client.post("/reports/transactions", json={"user": "Lorensius", "role": "admin"})
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert isinstance(data["data"], list)

# 5️⃣ Test mahasiswa tidak bisa akses laporan
def test_student_cannot_access_reports():
    response = client.post("/reports/transactions", json={"user": "Alice", "role": "student"})
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "error"
    assert "Access denied" in data["message"]
