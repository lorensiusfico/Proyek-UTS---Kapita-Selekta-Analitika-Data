# tests/test_api.py
from fastapi.testclient import TestClient
from main import app
from modules.library.storage import repository
from modules.library.schema.schemas import MAX_LOAN_DAYS
from datetime import date, timedelta
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_data():
    """Fixture untuk mereset data sebelum setiap test."""
    repository.reset_data()
    # Pastikan data di repository bersih
    assert len(repository.get_all_books()) == 0
    yield # Test dijalankan
    repository.reset_data()

# --- Test CRUD Buku (Admin) ---

def test_create_book():
    response = client.post(
        "/admin/books/",
        json={"title": "Test Book 1", "author": "Tester", "isbn": "123-456", "stock": 5}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book 1"
    assert data["book_id"] == 1
    assert data["stock"] == 5
    assert data["available_stock"] == 5

def test_read_books_empty():
    response = client.get("/admin/books/")
    assert response.status_code == 200
    assert response.json() == []

# ... Tambahkan test untuk read_book, update_book, delete_book ...

# --- Test Peminjaman (Mahasiswa) ---

def setup_book():
    """Fungsi helper untuk membuat buku yang akan dipinjam."""
    return client.post(
        "/admin/books/",
        json={"title": "Laskar Pelangi", "author": "Andrea Hirata", "isbn": "111-222", "stock": 2}
    ).json()

def test_borrow_book_success():
    book = setup_book()
    book_id = book["book_id"]

    response = client.post(
        "/loans/borrow",
        json={"book_id": book_id, "student_id": "NIM001"}
    )
    assert response.status_code == 201
    loan = response.json()
    assert loan["book_id"] == book_id
    assert loan["student_id"] == "NIM001"
    assert loan["is_active"] is True

    # Cek stok berkurang
    book_check = client.get(f"/admin/books/{book_id}").json()
    assert book_check["available_stock"] == 1 # Awal 2, pinjam 1 -> sisa 1

def test_borrow_book_stock_empty():
    book = setup_book()
    book_id = book["book_id"]
    
    # Pinjam buku sampai stok habis
    client.post("/loans/borrow", json={"book_id": book_id, "student_id": "NIM001"})
    client.post("/loans/borrow", json={"book_id": book_id, "student_id": "NIM002"})

    response = client.post(
        "/loans/borrow",
        json={"book_id": book_id, "student_id": "NIM003"}
    )
    assert response.status_code == 400
    assert "stok kosong" in response.json()["detail"]

# --- Test Pengembalian & Denda ---

def setup_loan(book_id):
    """Helper untuk membuat pinjaman aktif."""
    return client.post(
        "/loans/borrow",
        json={"book_id": book_id, "student_id": "NIM001"}
    ).json()

def test_return_book_on_time():
    book = setup_book()
    loan = setup_loan(book["book_id"])
    loan_id = loan["loan_id"]

    # Simulasikan pengembalian hari ini (On Time)
    response = client.put(f"/loans/return/{loan_id}")
    assert response.status_code == 200
    returned_loan = response.json()
    
    assert returned_loan["is_active"] is False
    assert returned_loan["delay_days"] == 0
    assert returned_loan["fine_amount"] == 0
    
    # Cek stok bertambah
    book_check = client.get(f"/admin/books/{book["book_id"]}").json()
    assert book_check["available_stock"] == 2 # Setelah pinjam 1, kembali 1 -> sisa 2

def test_return_book_overdue():
    book = setup_book()
    loan = setup_loan(book["book_id"])
    loan_id = loan["loan_id"]
    
    # Secara manual ubah due_date menjadi masa lalu (simulasi)
    past_date = date.today() - timedelta(days=5) # 5 hari overdue
    repository.update_loan(loan_id, {"due_date": past_date.isoformat()})

    response = client.put(f"/loans/return/{loan_id}")
    assert response.status_code == 200
    returned_loan = response.json()
    
    fine_rate = 1000 # dari schemas.py
    delay_days = 5
    expected_fine = delay_days * fine_rate

    assert returned_loan["is_active"] is False
    assert returned_loan["delay_days"] == delay_days
    assert returned_loan["fine_amount"] == expected_fine

# ... Tambahkan test untuk perpanjangan, laporan ...