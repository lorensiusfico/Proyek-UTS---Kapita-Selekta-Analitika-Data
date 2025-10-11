from fastapi import APIRouter, Header, HTTPException, Query
from datetime import date, timedelta, datetime

from library_management_api.modules.storage.repository import LOANS
from library_management_api.modules.services.services import calc_fine  #pastikan ada fungsi ini

router = APIRouter(prefix="/reports", tags=["reports"])

def require_admin(x_role: str):
    if x_role != "admin":
        raise HTTPException(403, "Admin only")

def recompute_fines(today: date | None = None) -> None:
    """Update field 'fine' untuk semua loan yang BELUM dikembalikan.
    Denda = 0 jika belum lewat due_date; >0 jika overdue.
    """
    if today is None:
        today = date.today()
    for loan in LOANS.values():
        if loan["returned_date"] is None:  #hanya loan aktif
            loan["fine"] = calc_fine(loan["due_date"], today)

@router.get("/active-loans")
def active_loans(x_role: str = Header(..., alias="X-Role")):
    require_admin(x_role)
    recompute_fines()  #pastikan denda up-to-date
    return [l for l in LOANS.values() if l["returned_date"] is None]

@router.get("/overdue")
def overdue(x_role: str = Header(..., alias="X-Role")):
    require_admin(x_role)
    recompute_fines()  #pastikan denda up-to-date
    today = date.today()
    return [l for l in LOANS.values() if l["returned_date"] is None and l["due_date"] < today]


@router.post("/_debug/set-due/{loan_id}")
def debug_set_due(
    loan_id: str,
    days_ago: int = Query(1, ge=1, description="Mundur berapa hari dari hari ini"),
    x_role: str = Header(..., alias="X-Role"),
):
    """
    Admin-only. Memundurkan due_date agar jadi overdue untuk pengujian.
    start_date ikut diset ulang supaya: due_date = start_date + total_days_allowed.
    Denda (fine) ikut dihitung ulang.
    """
    require_admin(x_role)
    loan = LOANS.get(loan_id)
    if not loan:
        raise HTTPException(404, "Loan not found")
    if loan["returned_date"] is not None:
        raise HTTPException(400, "Loan already returned")

    #due baru = hari ini - days_ago
    new_due = date.today() - timedelta(days=days_ago)
    #start baru = due baru - total_days_allowed
    allowed = loan["total_days_allowed"]
    new_start = new_due - timedelta(days=allowed)

    loan["due_date"] = new_due
    loan["start_date"] = new_start

    #hitung ulang fine untuk loan ini saja (atau panggil recompute_fines())
    loan["fine"] = calc_fine(loan["due_date"], date.today())
    return loan