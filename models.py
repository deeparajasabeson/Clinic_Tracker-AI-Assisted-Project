"""Data models: the plain records used by every other part."""


class Appointment:
    """A single clinic appointment.

    Should hold: id, patient name, date and time, reason, status
    (scheduled / completed / cancelled).
    Should be convertible to and from a plain dict for storage.
    """


class Expense:
    """A single clinic expense.

    Should hold: id, date, category, description, amount.
    Should be convertible to and from a plain dict for storage.
    """
