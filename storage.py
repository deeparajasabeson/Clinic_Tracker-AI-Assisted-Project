"""Storage: saves and loads records as JSON files in the data/ folder."""


def load_appointments():
    """Read data/appointments.json and return a list of Appointment objects.
    Should return an empty list if the file does not exist yet."""


def save_appointments(appointments):
    """Write the full list of Appointment objects to data/appointments.json."""


def load_expenses():
    """Read data/expenses.json and return a list of Expense objects.
    Should return an empty list if the file does not exist yet."""


def save_expenses(expenses):
    """Write the full list of Expense objects to data/expenses.json."""


def next_id(records):
    """Return the next unused integer id for a list of records."""
