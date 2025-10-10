from fastapi import FastAPI
from library.routes import books, loans, reports

app = FastAPI(title="📚 Library Management API", version="1.1")

app.include_router(books.router)
app.include_router(loans.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Library Management API"}
