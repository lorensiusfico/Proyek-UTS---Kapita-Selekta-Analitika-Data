import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime, timedelta

client = TestClient(app)

# Test: Mendapatkan daftar buku
def test_get_books():
    response = client.get("/admin/books")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Pastikan ada data buku yang dikembalikan

# Test: Menambahkan buku
def test_add_book():
    new_book = {
        "id": 11,
        "title": "New Book Title",
        "author": "New Author",
        "category": "Programming",
        "stock": 3
    }
    response = client.post("/admin/books", json=new_book)
    assert response.status_code == 200
    assert response.json()["title"] == new_book["title"]
    assert response.json()["author"] == new_book["author"]

# Test: Memperbarui buku
def test_update_book():
    updated_book = {
        "id": 1,
        "title": "Updated Title",
        "author": "Updated Author",
        "category": "Fiction",
        "stock": 10
    }
    response = client.put("/admin/books/1", json=updated_book)
    assert response.status_code == 200
    assert response.json()["title"] == updated_book["title"]
    assert response.json()["author"] == updated_book["author"]

# Test: Menghapus buku
def test_delete_book():
    response = client.delete("/admin/books/11")  # Menghapus buku yang ditambahkan di test_add_book
    assert response.status_code == 200
    assert response.json()["message"] == "Buku berhasil dihapus"

# Test: Pinjam buku
def test_borrow_book():
    loan_data = {
        "user_id": 1,
        "book_id": 1,
        "borrow_date": (datetime.now() - timedelta(days=5)).isoformat(),  # 5 hari yang lalu
        "return_date": (datetime.now() + timedelta(days=25)).isoformat(),  # 25 hari lagi
    }
    response = client.post("/student/borrow", json=loan_data)
    assert response.status_code == 200
    assert "Buku dikembalikan" in response.json()["message"]

# Test: Mengembalikan buku dan menghitung denda
def test_return_book():
    loan_data = {
        "user_id": 1,
        "book_id": 1,
        "borrow_date": (datetime.now() - timedelta(days=35)).isoformat(),  # 35 hari yang lalu
        "return_date": datetime.now().isoformat(),  # Hari ini
    }
    response = client.post("/student/return", json=loan_data)
    assert response.status_code == 200
    assert "fine" in response.json()  # Pastikan denda ada dalam respon

# Test: Laporan buku terlambat
def test_generate_report():
    response = client.get("/admin/reports?user_id=1")
    assert response.status_code == 200
    assert "overdue_books" in response.json()  # Pastikan ada laporan buku terlambat
    assert "total_fine" in response.json()  # Pastikan total denda dihitung

