from fastapi import APIRouter
from datetime import date
from pydantic import BaseModel
from library.schemas.schema import BorrowRequest, ReturnRequest, ExtendRequest, UserRoleRequest
from library.services.service import (
    borrow_book, return_book, extend_borrow, format_response,
    set_today_override, clear_today_override, advance_today, today, get_today_override, get_user_role
)
from library.storages.repository import transactions

router = APIRouter(prefix="/loans", tags=["Loans"])

# ===== Operasi utama =====
@router.post("/borrow")
def borrow(req: BorrowRequest):
    return borrow_book(req.user, req.book_id)

@router.post("/return")
def return_borrowed(req: ReturnRequest):
    return return_book(req.user, req.book_id)

@router.post("/extend")
def extend(req: ExtendRequest):
    return extend_borrow(req.user, req.book_id, req.extend_days)

# ===== Debug Clock (khusus admin) =====
class ClockSetRequest(UserRoleRequest):
    date: date

class ClockAdvanceRequest(UserRoleRequest):
    days: int

@router.post("/debug/clock/set")
def debug_clock_set(req: ClockSetRequest):
    role = get_user_role(req.user)
    if role != "admin":
        return format_response("error", "Access denied", error="Only admin can set debug clock")

    set_today_override(req.date)
    return format_response("success", "Clock set", data={"today": str(today())})

@router.post("/debug/clock/advance")
def debug_clock_advance(req: ClockAdvanceRequest):
    role = get_user_role(req.user)
    if role != "admin":
        return format_response("error", "Access denied", error="Only admin can advance debug clock")

    advance_today(req.days)
    return format_response("success", f"Clock advanced by {req.days} days", data={"today": str(today())})

@router.post("/debug/clock/clear")
def debug_clock_clear(req: UserRoleRequest):
    role = get_user_role(req.user)
    if role != "admin":
        return format_response("error", "Access denied", error="Only admin can clear debug clock")

    clear_today_override()
    return format_response("success", "Clock cleared", data={"today": str(today())})

@router.get("/debug/clock")
def debug_clock_status(req: UserRoleRequest):
    role = get_user_role(req.user)
    if role != "admin":
        return format_response("error", "Access denied", error="Only admin can view debug clock status")

    return format_response(
        "success",
        "Clock status",
        data={"today": str(today()), "overridden": get_today_override() is not None}
    )
