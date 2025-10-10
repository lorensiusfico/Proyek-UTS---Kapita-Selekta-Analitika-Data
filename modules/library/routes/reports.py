# modules/routes/reports.py
from fastapi import APIRouter
from typing import List

from modules.library.schema.schemas import ReportLoan
from modules.library.services import services

router = APIRouter(prefix="/admin/reports", tags=["Admin: Laporan"])

@router.get("/active-overdue", response_model=List[ReportLoan])
def get_active_and_overdue_loans():
    """Melihat daftar pinjaman aktif, termasuk yang sudah jatuh tempo (overdue) (Admin)."""
    report_data = services.get_active_and_overdue_loans_report()
    return [ReportLoan.model_validate(r) for r in report_data]