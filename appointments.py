"""Appointment logic: booking and managing appointments."""


def add_appointment(patient, when, reason):
    """Create and save a new scheduled appointment.
    Should validate inputs and refuse to double-book the same time slot."""


def list_appointments(date=None, status=None):
    """Return appointments, optionally filtered by date and/or status."""


def get_day_schedule(date):
    """Return the scheduled appointments for one day, sorted by time."""


def cancel_appointment(appointment_id):
    """Mark an appointment as cancelled. Should fail if the id is unknown."""


def reschedule_appointment(appointment_id, new_when):
    """Move an appointment to a new time.
    Should apply the same double-booking check as add_appointment."""


def complete_appointment(appointment_id):
    """Mark an appointment as completed."""


def is_slot_free(when, ignore_id=None):
    """Return True if no scheduled appointment already uses this time.
    ignore_id lets a reschedule skip the appointment being moved."""
