
from datetime import datetime, date


def calculate_dday(due_date):
    due = datetime.strptime(due_date, "%Y-%m-%d").date()
    today = date.today()
    return (due - today).days


def sort_by_deadline(schedules):
    return sorted(schedules, key=lambda s: s["due_date"])


def sort_by_priority(schedules):
    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2
    }
    return sorted(
        schedules,
        key=lambda s: priority_order[s["priority"]]
    )
