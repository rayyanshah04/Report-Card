"""
Utility helper functions
"""
from datetime import datetime


def format_date(date_str):
    """Format date from YYYY-MM-DD or YYYY-MM-DD HH:MM:SS to 'D Month YYYY'"""
    if not date_str:
        return "N/A"
    try:
        if " " in date_str:
            date_obj = datetime.strptime(date_str.split()[0], "%Y-%m-%d")
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        day = date_obj.day
        month = date_obj.strftime("%B")
        year = date_obj.year
        return f"{day} {month} {year}"
    except Exception:  # pragma: no cover
        return date_str


def calculate_age(date_of_birth):
    """Calculate age from date of birth"""
    if not date_of_birth:
        return "N/A"
    try:
        date_part = date_of_birth.split()[0] if " " in date_of_birth else date_of_birth
        dob = datetime.strptime(date_part, "%Y-%m-%d")
        today = datetime.now()
        age_years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        age_months = (today.year - dob.year) * 12 + today.month - dob.month
        if today.day < dob.day:
            age_months -= 1
        return f"{age_years} years ({age_months} months)"
    except Exception:  # pragma: no cover
        return "N/A"


def calculate_years_studying(joining_date):
    """Calculate years studying from joining date"""
    if not joining_date:
        return "N/A"
    try:
        date_part = joining_date.split()[0] if " " in joining_date else joining_date
        join_date = datetime.strptime(date_part, "%Y-%m-%d")
        today = datetime.now()
        years = today.year - join_date.year - ((today.month, today.day) < (join_date.month, join_date.day))
        months = (today.year - join_date.year) * 12 + today.month - join_date.month
        if today.day < join_date.day:
            months -= 1
        return f"{years} years {months % 12} months"
    except Exception:  # pragma: no cover
        return "N/A"
