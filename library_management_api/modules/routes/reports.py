from fastapi import APIRouter, Header, HTTPException
from datetime import date
from library_management_api.modules.storage.repository import LOANS

router = APIRouter(prefix="/reports", tags=["reports"])

def require_admin(x_role: str):
    if x_role != "admin":
        raise HTTPException(403, "Admin only")

@router.get("/active-loans")
def active_loans(x_role: str = Header(..., alias="X-Role")):
    require_admin(x_role)
    return [l for l in LOANS.values() if l["returned_date"] is None]

@router.get("/overdue")
def overdue(x_role: str = Header(..., alias="X-Role")):
    require_admin(x_role)
    today = date.today()
    return [l for l in LOANS.values() if l["returned_date"] is None and l["due_date"] < today]
