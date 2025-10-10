from fastapi.testclient import TestClient
from datetime import date, timedelta
from copy import deepcopy

from main import app 

#pakai repository.py sebagai storage in-memory
from library_management_api.modules.storage import repository as repo

client = TestClient(app)

#reset in-place: router & test tetap pakai object dict yang sama
_INITIAL_BOOKS = deepcopy(repo.BOOKS)
_INITIAL_LOANS = deepcopy(repo.LOANS)
_INITIAL_SEQ = deepcopy(repo.SEQ) if hasattr(repo, "SEQ") else None

def reset_repo():
    #reset BOOKS
    repo.BOOKS.clear()
    repo.BOOKS.update(deepcopy(_INITIAL_BOOKS))
    #reset LOANS
    repo.LOANS.clear()
    repo.LOANS.update(deepcopy(_INITIAL_LOANS))
    #reset SEQ kalau ada
    if _INITIAL_SEQ is not None and hasattr(repo, "SEQ"):
        repo.SEQ.clear()
        repo.SEQ.update(deepcopy(_INITIAL_SEQ))

# 1.) list buku (happy path)
def test_list_books_ok():
    reset_repo()
    r = client.get("/books", headers={"X-Role": "student", "X-User-Id": "S123"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)

# 2.) alur pinjam → perpanjang → kembali (happy path)
def test_borrow_and_return():
    reset_repo()
    #borrow
    r = client.post(
        "/loans",
        json={"book_id": "B001", "days": 7},
        headers={"X-Role": "student", "X-User-Id": "S999"},
    )
    assert r.status_code == 200
    loan_id = r.json()["loan_id"]

    #extend
    r2 = client.post(
        f"/loans/{loan_id}/extend",
        params={"extra_days": 5},
        headers={"X-Role": "student", "X-User-Id": "S999"},
    )
    assert r2.status_code == 200
    assert r2.json()["total_days_allowed"] == 12

    #return
    r3 = client.post(
        f"/loans/{loan_id}/return",
        headers={"X-Role": "student", "X-User-Id": "S999"},
    )
    assert r3.status_code == 200
    assert r3.json()["returned_date"] is not None

# 3.) admin bisa CRUD buku, dan efeknya terlihat
def test_admin_can_create_update_delete_book():
    reset_repo()
    #create
    r = client.post(
        "/books",
        json={
            "title": "Refactoring",
            "author": "Martin Fowler",
            "year": 2018,
            "stock": 3,
        },
        headers={"X-Role": "admin"},
    )
    assert r.status_code == 200
    book_id = r.json()["book_id"]

    #update
    r2 = client.patch(
        f"/books/{book_id}",
        json={
            "title": "Refactoring (2nd)",
            "author": "Martin Fowler",
            "year": 2018,
            "stock": 5,
        },
        headers={"X-Role": "admin"},
    )
    assert r2.status_code == 200
    assert r2.json()["stock"] == 5

    #delete
    r3 = client.delete(f"/books/{book_id}", headers={"X-Role": "admin"})
    assert r3.status_code == 200

    #pastikan sudah terhapus
    r4 = client.get("/books", headers={"X-Role": "student", "X-User-Id": "S1"})
    ids = [b["book_id"] for b in r4.json()]
    assert book_id not in ids

# 4.) student tidak boleh akses endpoint admin
def test_student_blocked_on_admin_routes():
    reset_repo()
    r = client.post(
        "/books",
        json={"title": "Should Fail", "author": "X", "year": 2024, "stock": 1},
        headers={"X-Role": "student", "X-User-Id": "S1"},
    )
    assert r.status_code == 403

# 5.) pinjam buku stok 0 ditolak
def test_borrow_out_of_stock():
    reset_repo()
    target_id = "B002" if "B002" in repo.BOOKS else next(iter(repo.BOOKS.keys()))
    #set stok buku 0 IN-PLACE
    repo.BOOKS[target_id]["stock"] = 0

    r = client.post(
        "/loans",
        json={"book_id": target_id, "days": 7},
        headers={"X-Role": "student", "X-User-Id": "S11"},
    )
    assert r.status_code == 400
    assert "Out of stock" in r.text

# 6.) perpanjang melebihi total 30 hari ditolak
def test_extend_rejects_over_30_days_total():
    reset_repo()
    book = "B003" if "B003" in repo.BOOKS else list(repo.BOOKS)[0]
    r = client.post(
        "/loans",
        json={"book_id": book, "days": 14},
        headers={"X-Role": "student", "X-User-Id": "S12"},
    )
    assert r.status_code == 200
    loan_id = r.json()["loan_id"]

    r2 = client.post(
        f"/loans/{loan_id}/extend",
        params={"extra_days": 20},
        headers={"X-Role": "student", "X-User-Id": "S12"},
    )
    assert r2.status_code == 400

# 7.) pengembalian telat → denda sesuai hari
def test_return_with_overdue_fine():
    reset_repo()
    book = "B004" if "B004" in repo.BOOKS else list(repo.BOOKS)[0]
    r = client.post(
        "/loans",
        json={"book_id": book, "days": 1},
        headers={"X-Role": "student", "X-User-Id": "S13"},
    )
    assert r.status_code == 200
    loan_id = r.json()["loan_id"]

    #ubah due_date IN-PLACE pada dict yang sama dipakai router
    repo.LOANS[loan_id]["due_date"] = date.today() - timedelta(days=3)

    r2 = client.post(
        f"/loans/{loan_id}/return",
        headers={"X-Role": "student", "X-User-Id": "S13"},
    )
    assert r2.status_code == 200
    assert r2.json()["fine"] == 3000  # 3 * 1000

# 8.) reports admin: active-loans & overdue
def test_reports_endpoints():
    reset_repo()
    #1 aktif
    r1 = client.post(
        "/loans",
        json={"book_id": list(repo.BOOKS)[0], "days": 7},
        headers={"X-Role": "student", "X-User-Id": "S20"},
    )
    assert r1.status_code == 200

    #1 overdue
    r2 = client.post(
        "/loans",
        json={"book_id": list(repo.BOOKS)[1], "days": 1},
        headers={"X-Role": "student", "X-User-Id": "S21"},
    )
    loan_overdue = r2.json()["loan_id"]
    #set telat 1 hari IN-PLACE
    repo.LOANS[loan_overdue]["due_date"] = date.today() - timedelta(days=1)

    a = client.get("/reports/active-loans", headers={"X-Role": "admin"})
    assert a.status_code == 200
    assert any(l["returned_date"] is None for l in a.json())

    o = client.get("/reports/overdue", headers={"X-Role": "admin"})
    assert o.status_code == 200
    assert any(l["loan_id"] == loan_overdue for l in o.json())

# 9.) validasi header: student tanpa X-User-Id → 400
def test_student_missing_user_id_header():
    reset_repo()
    r = client.post(
        "/loans",
        json={"book_id": "B001", "days": 7},
        headers={"X-Role": "student"},  #tidak kirim X-User-Id
    )
    assert r.status_code == 400