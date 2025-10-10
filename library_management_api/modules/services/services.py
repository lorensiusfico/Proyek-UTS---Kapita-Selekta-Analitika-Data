from datetime import date, timedelta

FINE_PER_DAY = 1000
MAX_TOTAL_DAYS = 30

def calc_due_date(start_date: date, days: int) -> date:
    return start_date + timedelta(days=days)

def can_extend(current_total_allowed: int, extra_days: int) -> bool:
    return current_total_allowed + extra_days <= MAX_TOTAL_DAYS

def calc_fine(due_date: date, returned_date: date) -> int:
    if returned_date <= due_date:
        return 0
    return (returned_date - due_date).days * FINE_PER_DAY
