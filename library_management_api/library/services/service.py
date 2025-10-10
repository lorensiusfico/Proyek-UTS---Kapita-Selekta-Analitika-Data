from datetime import date, timedelta
from typing import Optional
from library.storages.repository import books, transactions, users

CURRENT_DATE_OVERRIDE: Optional[date] = None

def today() -> date:
    return CURRENT_DATE_OVERRIDE or date.today()

def set_today_override(d: date):
    global CURRENT_DATE_OVERRIDE
    CURRENT_DATE_OVERRIDE = d

def clear_today_override():
    global CURRENT_DATE_OVERRIDE
    CURRENT_DATE_OVERRIDE = None

def advance_today(days: int):
    global CURRENT_DATE_OVERRIDE
    CURRENT_DATE_OVERRIDE = (CURRENT_DATE_OVERRIDE or date.today()) + timedelta(days=days)

def get_today_override() -> Optional[date]:
    return CURRENT_DATE_OVERRIDE

def format_response(status: str, message: str, data=None, error=None):
    return {"status": status, "message": message, "data": data, "error": error}

def find_book(book_id):
    return next((b for b in books if b.id == book_id), None)

def get_user_role(username):
    for u in users:
        if u["name"].lower() == username.lower():
            return u["role"]
    return None

def borrow_book(user, book_id):
    book = find_book(book_id)
    if not book:
        return format_response("error", "Book not found", error="Invalid book ID")
    if book.stock <= 0:
        return format_response("error", "Book currently unavailable", error="Out of stock")
    for t in transactions:
        if t["user"] == user and t["book_id"] == book_id and t["return_date"] is None:
            return format_response("error", "Already borrowed", error="Duplicate borrow")

    book.stock -= 1
    borrow_date = today()
    due_date = borrow_date + timedelta(days=14)

    # Batas total 30 hari sejak borrow_date
    max_due = borrow_date + timedelta(days=30)
    if due_date > max_due:
        due_date = max_due

    transaction = {
        "user": user,
        "book_id": book_id,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "return_date": None,
        "fine": 0
    }
    transactions.append(transaction)
    return format_response("success", "Book borrowed successfully", data=transaction)

def return_book(user, book_id):
    for t in transactions:
        if t["user"] == user and t["book_id"] == book_id and t["return_date"] is None:
            t["return_date"] = today()
            delay = (t["return_date"] - t["due_date"]).days
            t["fine"] = delay * 1000 if delay > 0 else 0
            book = find_book(book_id)
            if book:
                book.stock += 1
            return format_response("success", "Book returned successfully", data=t)
    return format_response("error", "Transaction not found", error="Invalid return request")

def extend_borrow(user, book_id, extend_days):
    for t in transactions:
        if t["user"] == user and t["book_id"] == book_id and t["return_date"] is None:
            borrow_date = t["borrow_date"]
            max_due_date = borrow_date + timedelta(days=30)
            proposed_due_date = t["due_date"] + timedelta(days=extend_days)
            if proposed_due_date > max_due_date:
                return format_response(
                    "error",
                    "Extension exceeds 30-day limit",
                    error=f"Cannot extend beyond {max_due_date}"
                )
            t["due_date"] = proposed_due_date
            return format_response("success", "Extension successful", data=t)
    return format_response("error", "Transaction not found", error="Invalid extend request")