from datetime import date, timedelta

books = []
transactions = []

def format_response(status: str, message: str, data=None, error=None):
    return {
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }

def find_book(book_id):
    return next((b for b in books if b.id == book_id), None)

def add_book(book):
    if find_book(book.id):
        return format_response("error", "Book ID already exists", error="Duplicate ID")
    books.append(book)
    return format_response("success", "Book added successfully", data=book.dict())

def borrow_book(user, book_id):
    book = find_book(book_id)
    if not book:
        return format_response("error", "Book not found", error="Invalid book ID")
    if book.stock <= 0:
        return format_response("error", "Book currently unavailable", error="Out of stock")
    for t in transactions:
        if t["user"] == user and t["book_id"] == book_id and t["return_date"] is None:
            return format_response("error", "You have already borrowed this book", error="Duplicate borrow")

    book.stock -= 1
    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=14)
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
            t["return_date"] = date.today()
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
            total_days = (t["due_date"] - t["borrow_date"]).days + extend_days
            if total_days > 30:
                return format_response("error", "Extension exceeds 30-day limit", error="Over extension")
            t["due_date"] += timedelta(days=extend_days)
            return format_response("success", "Extension successful", data=t)
    return format_response("error", "Transaction not found", error="Invalid extend request")
