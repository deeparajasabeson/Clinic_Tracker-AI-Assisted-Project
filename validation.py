"""Input checks shared by the appointment and expense logic."""

import calendar
import math
from datetime import date, datetime

# Earliest date an entry may have.
MIN_DATE = date(2000, 1, 1)

# The clinic only takes bookings this many months ahead of today.
MAX_MONTHS_AHEAD = 3

# The only categories an entry may use.
VALID_CATEGORIES = ["Consultation", "Diagnostics", "Procedure", "Follow-up", "Pharmacy"]

# Lowercase copy, built once, for the capital-letters-ignored comparison.
_VALID_CATEGORIES_LOWER = {c.lower() for c in VALID_CATEGORIES}


def latest_allowed_date():
    """Return the last date that may be booked: today plus 3 months."""
    today = date.today()
    # Move forward by whole months, rolling over into the next year if needed.
    month_index = today.month - 1 + MAX_MONTHS_AHEAD
    year = today.year + month_index // 12
    month = month_index % 12 + 1
    # If the day does not exist in that month (e.g. 31 Nov), use its last day.
    day = min(today.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def _clean_text(value):
    """Return value as text with surrounding spaces removed.
    None, empty text and other "empty" values (0, False) become ''."""
    return str(value or "").strip()


def _parse_date(value):
    """Return value as a date, or None if it is not a real date.
    Accepts date / datetime objects, or text written as YYYY-MM-DD."""
    if isinstance(value, datetime):  # check first: datetime is a kind of date
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        return None


def check_entry(patient_ref, entry_date, category, cost):
    """Check one entry and return a list of problems (strings).
    An empty list means the entry is fine."""
    problems = []

    # Patient reference must not be empty or only spaces.
    if not _clean_text(patient_ref):
        problems.append("Patient reference is required.")

    # Date must be real, and inside the allowed range.
    parsed_date = _parse_date(entry_date)
    if parsed_date is None:
        problems.append("Date must be a real date in YYYY-MM-DD format.")
    else:
        latest = latest_allowed_date()
        if not MIN_DATE <= parsed_date <= latest:
            problems.append(
                f"Date must be between {MIN_DATE} and {latest} "
                f"(bookings open {MAX_MONTHS_AHEAD} months ahead)."
            )

    # Category must be one of the valid categories (capital letters ignored).
    category_text = _clean_text(category)
    if not category_text:
        problems.append("Category is required.")
    elif category_text.lower() not in _VALID_CATEGORIES_LOWER:
        problems.append("Category must be one of: " + ", ".join(VALID_CATEGORIES) + ".")

    # Cost must be a finite number (NaN and infinity are not real costs).
    # Zero is allowed, negative is refused.
    try:
        cost_number = float(cost)
    except (TypeError, ValueError):
        cost_number = None
    if cost_number is None or not math.isfinite(cost_number):
        problems.append("Cost must be a number.")
    elif cost_number < 0:
        problems.append("Cost cannot be negative.")

    return problems


def validate_date(value):
    """Check a date string is a real calendar date; return it parsed.
    Should raise ValueError with a clear message otherwise."""


def validate_datetime(value):
    """Check a date-and-time string is valid; return it parsed.
    Should raise ValueError with a clear message otherwise."""


def validate_name(value):
    """Check a patient name is not empty or only spaces; return it trimmed."""


def validate_amount(value):
    """Check an expense amount is a number greater than zero; return it."""
