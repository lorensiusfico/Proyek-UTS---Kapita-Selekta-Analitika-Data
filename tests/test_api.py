from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- Test Root Endpoint ---
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Welcome to Library Management API" in data["message"]

# --- Test CRUD Buku (Books) ---
def test_add_and_get_book():
    # Tambah buku baru
    new_book = {
        "id": 10,
        "title": "Data Analytics 101",
        "author": "Olas Team",
        "stock": 5
    }
    response = client.post("/books/", json=new_book)
    assert response.status_code == 200
    assert response.json()["title"] == "Data Analytics 101"

    # Ambil semua buku
    response = client.get("/books/")
    assert response.status_code == 200
    books = response.json()
    assert any(b["id"] == 10 for b in books)

    # Ambil buku berdasarkan ID
    response = client.get("/books/10")
    assert response.status_code == 200
    assert response.json()["author"] == "Olas Team"

    # Update buku
    updated_book = {
        "id": 10,
        "title": "Data Analytics Advanced",
        "author": "Olas Team",
        "stock": 10
    }
    response = client.put("/books/10", json=updated_book)
    assert response.status_code == 200
    assert response.json()["title"] == "Data Analytics Advanced"

    # Hapus buku
    response = client.delete("/books/10")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"

# --- Test Peminjaman Buku ---
def test_borrow_and_return_book():
    # Pinjam buku yang tersedia (id=1 dari dummy data)
    new_loan = {
        "id": 101,
        "book_id": 1,
        "user_id": 1
    }
    response = client.post("/loans/borrow", json=new_loan)
    assert response.status_code == 200
    loan_data = response.json()
    assert loan_data["book_id"] == 1
    assert loan_data["returned"] == False

    # Kembalikan buku
    response = client.put("/loans/return/101")
    assert response.status_code == 200
    assert "Book returned successfully" in response.json()["message"]

# --- Test Laporan Admin ---
def test_reports_active_and_overdue():
    response = client.get("/reports/active")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = client.get("/reports/overdue")
    assert response.status_code == 200
    assert isinstance(response.json(), list)