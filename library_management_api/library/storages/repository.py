from library.schemas.schema import Book

# Dummy data buku perpustakaan
books = [
    Book(id=1, title="Deep Learning", author="Ian Goodfellow", stock=3),
    Book(id=2, title="Python Machine Learning", author="Sebastian Raschka", stock=5),
    Book(id=3, title="Clean Code", author="Robert C. Martin", stock=2),
    Book(id=4, title="Data Science from Scratch", author="Joel Grus", stock=4),
    Book(id=5, title="Introduction to Algorithms", author="Thomas H. Cormen", stock=1),
]

users = [
    {"name": "Lorensius", "role": "admin"},
    {"name": "Alice", "role": "student"},
    {"name": "Bob", "role": "student"},
]

transactions = []
