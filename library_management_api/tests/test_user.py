from fastapi.testclient import TestClient
from library_management_api.main import app

client = TestClient(app)

def test_add_book():
    response = client.post("/admin/books", json={"id": 1, "title": "AI 101", "author": "John", "stock": 3})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_borrow_book():
    response = client.post("/student/borrow", json={"user": "Alice", "book_id": 1})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
