"""Expense logic: recording and summarising clinic spending."""


def add_expense(date, category, description, amount):
    """Validate and save a new expense."""


def list_expenses(start_date=None, end_date=None, category=None):
    """Return expenses, optionally filtered by date range and/or category."""


def total_by_category(start_date=None, end_date=None):
    """Return a dict of category -> total amount for the given range."""


def total_by_month(year):
    """Return a dict of month -> total amount for the given year."""


def delete_expense(expense_id):
    """Remove an expense. Should fail if the id is unknown."""
