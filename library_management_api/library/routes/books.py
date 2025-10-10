from fastapi import APIRouter
from library.schemas.schema import UserRoleRequest
from library.storages.repository import books
from library.services.service import format_response, get_user_role

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/add")
def add_book(req: UserRoleRequest):
    role = get_user_role(req.user)
    if role != "admin":
        return format_response("error", "Access denied", error="Only admin can add books")
    return format_response("success", "Admin verified", data={"role": role})

@router.get("/")
def list_all_books():
    return format_response("success", "All books retrieved", data=[b.dict() for b in books])
