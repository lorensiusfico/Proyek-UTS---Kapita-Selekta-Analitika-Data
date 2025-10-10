from fastapi import APIRouter
from datetime import date
from typing import List
from modules.library.schema.schemas import Loan

router = APIRouter()

# Data dummy — biasanya diambil dari loans_db
loans_db: List[Loan] = []

@router.get("/active", response_model=List[Loan])
def get_active_loans():
    active = [loan for loan in loans_db if not loan.returned]
    return active

@router.get("/overdue", response_model=List[Loan])
def get_overdue_loans():
    overdue = [loan for loan in loans_db if not loan.returned and loan.due_date < date.today()]
    return overdue