from fastapi import APIRouter
from library.schemas.schema import UserRoleRequest
from library.storages.repository import transactions
from library.services.service import format_response, get_user_role, today

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/transactions")
def get_all_transactions(req: UserRoleRequest):
    role = get_user_role(req.user)
    if role != "admin":
        return format_response("error", "Access denied", error="Only admin can view reports")
    return format_response("success", "Transaction history retrieved", data=transactions)

@router.post("/overdue")
def get_overdue_transactions(req: UserRoleRequest):
    """
    Hanya admin yang dapat melihat daftar transaksi yang sudah melewati tanggal jatuh tempo
    tetapi belum dikembalikan.
    """
    role = get_user_role(req.user)
    if role != "admin":
        return format_response("error", "Access denied", error="Only admin can view overdue reports")

    current_date = today()
    overdue_list = []

    for t in transactions:
        if t["return_date"] is None and current_date > t["due_date"]:
            days_overdue = (current_date - t["due_date"]).days
            current_fine = days_overdue * 1000
            overdue_list.append({
                "user": t["user"],
                "book_id": t["book_id"],
                "borrow_date": t["borrow_date"],
                "due_date": t["due_date"],
                "days_overdue": days_overdue,
                "expected_fine": current_fine
            })

    if not overdue_list:
        return format_response("success", "No overdue transactions found", data=[])

    return format_response(
        "success",
        f"Found {len(overdue_list)} overdue transaction(s)",
        data=overdue_list
    )