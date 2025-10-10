from fastapi import APIRouter
from typing import List
from library.schema.schemas import Report
from library.services.services import generate_report
from library.storage.repository import generate_report

router = APIRouter()

@router.get("/reports")
def generate_report(user_id: int):
    return generate_report(user_id)


@router.get("/reports", response_model=List[Report])
def get_reports():
    return generate_report()  # Mengambil data laporan
