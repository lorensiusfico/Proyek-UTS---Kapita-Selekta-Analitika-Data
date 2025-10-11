from fastapi import APIRouter, Header, HTTPException
from datetime import date
from library_management_api.modules.schema.schemas import LoanCreate, Loan
from library_management_api.modules.storage.repository import BOOKS, LOANS, new_loan_id
from library_management_api.modules.services.services import calc_due_date, can_extend, calc_fine, MAX_TOTAL_DAYS

router = APIRouter(prefix="/loans", tags=["loans"])

def require_student(x_role: str, x_user_id: str | None):
    if x_role != "student":
        raise HTTPException(403, "Student only")
    if not x_user_id:
        raise HTTPException(400, "X-User-Id required")

@router.post("", response_model=Loan)
def borrow(payload: LoanCreate, x_role: str = Header(..., alias="X-Role"), x_user_id: str | None = Header(None, alias="X-User-Id")):
    require_student(x_role, x_user_id)
    if payload.book_id not in BOOKS:
        raise HTTPException(404, "Book not found")
    if BOOKS[payload.book_id]["stock"] <= 0:
        raise HTTPException(400, "Out of stock")
    start = date.today()
    due = calc_due_date(start, payload.days)
    loan_id = new_loan_id()
    LOANS[loan_id] = {
        "loan_id": loan_id,
        "book_id": payload.book_id,
        "user_id": x_user_id,
        "start_date": start,
        "due_date": due,
        "total_days_allowed": payload.days,  #awal
        "returned_date": None,
        "fine": 0,
        "paid": False,
        "paid_at": None
    }
    BOOKS[payload.book_id]["stock"] -= 1
    return LOANS[loan_id]

@router.post("/{loan_id}/extend", response_model=Loan)
def extend(loan_id: str, extra_days: int, x_role: str = Header(..., alias="X-Role"), x_user_id: str | None = Header(None, alias="X-User-Id")):
    require_student(x_role, x_user_id)
    loan = LOANS.get(loan_id)
    if not loan or loan["user_id"] != x_user_id:
        raise HTTPException(404, "Loan not found")
    if loan["returned_date"] is not None:
        raise HTTPException(400, "Loan already returned")
    if not can_extend(loan["total_days_allowed"], extra_days):
        raise HTTPException(400, f"Max total {MAX_TOTAL_DAYS} days")
    loan["total_days_allowed"] += extra_days
    #due date baru = start_date + total_days_allowed
    loan["due_date"] = calc_due_date(loan["start_date"], loan["total_days_allowed"])
    return loan

@router.post("/{loan_id}/return", response_model=Loan)
def return_book(loan_id: str, x_role: str = Header(..., alias="X-Role"), x_user_id: str | None = Header(None, alias="X-User-Id")):
    require_student(x_role, x_user_id)
    loan = LOANS.get(loan_id)
    if not loan or loan["user_id"] != x_user_id:
        raise HTTPException(404, "Loan not found")
    if loan["returned_date"] is not None:
        raise HTTPException(400, "Already returned")
    returned = date.today()
    loan["returned_date"] = returned
    loan["fine"] = calc_fine(loan["due_date"], returned)
    #kembalikan stok
    BOOKS[loan["book_id"]]["stock"] += 1
    return loan

def require_student_or_admin(x_role: str, x_user_id: str | None, loan_user_id: str):
    if x_role == "admin":
        return
    if x_role == "student" and x_user_id == loan_user_id:
        return
    raise HTTPException(403, "Not allowed")

@router.post("/loans/{loan_id}/pay")
def pay_fine(
    loan_id: str,
    x_role: str = Header(..., alias="X-Role"),
    x_user_id: str | None = Header(None, alias="X-User-Id"),
):
    """
    Menandai denda sudah dibayar.
    Hanya boleh oleh admin atau pemilik loan (student yg sama).
    Hanya bisa setelah buku dikembalikan.
    """
    loan = LOANS.get(loan_id)
    if not loan:
        raise HTTPException(404, "Loan not found")

    #hanya admin atau pemilik loan
    require_student_or_admin(x_role, x_user_id, loan["user_id"])

    #wajib sudah dikembalikan dulu
    if loan["returned_date"] is None:
        raise HTTPException(400, "Return the book first")

    #set pembayaran
    loan["paid"] = True
    loan["paid_at"] = date.today()
    return loan
