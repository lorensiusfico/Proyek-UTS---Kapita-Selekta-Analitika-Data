from datetime import date, timedelta
from modules.library.schema.schemas import Loan

# Konstanta sistem
MAX_LOAN_DAYS = 30
DAILY_FINE = 2000  # denda per hari

# Hitung tanggal jatuh tempo peminjaman (default 7 hari)
def calculate_due_date(start_date: date, extend_days: int = 7) -> date:
    return start_date + timedelta(days=extend_days)

# Hitung total keterlambatan dan denda
def calculate_fine(loan: Loan) -> int:
    if loan.returned:
        delay_days = (date.today() - loan.due_date).days
        loan.late_days = max(0, delay_days)
        loan.fine = loan.late_days * DAILY_FINE
        return loan.fine
    return 0

# Cek apakah masih bisa diperpanjang
def can_extend(loan: Loan) -> bool:
    total_days = (loan.due_date - loan.start_date).days
    return total_days < MAX_LOAN_DAYS