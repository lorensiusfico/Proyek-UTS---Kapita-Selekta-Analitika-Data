from datetime import date

#database
BOOKS: dict[str, dict] = {
    "B001": {"book_id": "B001", "title": "Clean Code", "author": "Robert C. Martin", "year": 2008, "stock": 3},
    "B002": {"book_id": "B002", "title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "year": 2009, "stock": 2},
    "B003": {"book_id": "B003", "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "year": 1999, "stock": 4},
    "B004": {"book_id": "B004", "title": "Design Patterns: Elements of Reusable Object-Oriented Software", "author": "Erich Gamma", "year": 1994, "stock": 3},
    "B005": {"book_id": "B005", "title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "year": 2020, "stock": 5},
    "B006": {"book_id": "B006", "title": "Deep Learning", "author": "Ian Goodfellow", "year": 2016, "stock": 2},
    "B007": {"book_id": "B007", "title": "Data Science from Scratch", "author": "Joel Grus", "year": 2019, "stock": 3},
    "B008": {"book_id": "B008", "title": "Python Crash Course", "author": "Eric Matthes", "year": 2023, "stock": 6},
    "B009": {"book_id": "B009", "title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "year": 2011, "stock": 4},
    "B010": {"book_id": "B010", "title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "year": 2013, "stock": 2},
}

#pinjaman buku (kosong saat awal)
LOANS: dict[str, dict] = {}

#counter ID otomatis
SEQ = {"book": 10, "loan": 1}


#add book
def new_book_id() -> str:
    """Generate ID buku baru (B011, B012, dst)."""
    SEQ["book"] += 1
    return f"B{SEQ['book']:03d}"

#add loan
def new_loan_id() -> str:
    """Generate ID peminjaman baru (L0002, L0003, dst)."""
    i = SEQ["loan"]
    SEQ["loan"] += 1
    return f"L{i:04d}"
