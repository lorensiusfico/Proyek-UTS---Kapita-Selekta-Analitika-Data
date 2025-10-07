from fastapi import FastAPI
from routes import admin, student

app = FastAPI(title="📚 Library Management API", version="1.0")

app.include_router(admin.router)
app.include_router(student.router)

@app.get("/")
def root():
    return {"message": "Welcome to Library Management API"}
