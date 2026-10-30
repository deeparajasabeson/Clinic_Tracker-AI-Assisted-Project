"""Command-line tester for check_entry.

Check one entry:
    python try_check_entry.py PT-001 2026-08-03 Consultation 120.00

Run the built-in sample cases:
    python try_check_entry.py --samples
"""

import sys
from datetime import date, timedelta

from validation import check_entry, latest_allowed_date

# (patient_ref, date, category, cost, should_be_ok)
SAMPLES = [
    ("PT-001", "2026-08-03", "Consultation", "120.00", True),   # normal entry
    ("PT-002", "2026-08-03", "Pharmacy", "0", True),            # zero cost is allowed
    ("PT-003", "2026-08-03", "follow-up", "45", True),          # capital letters ignored
    ("PT-004", "2026-08-03", "Procedure", "-5", False),         # negative cost
    ("PT-005", "2026-13-40", "Diagnostics", "80", False),       # impossible date
    ("PT-009", "1850-05-10", "Consultation", "80", False),      # year too old
    ("PT-010", "1099-05-10", "Consultation", "80", False),      # year too old
    ("PT-011", "2999-01-01", "Consultation", "80", False),      # far in the future
    ("PT-012", str(latest_allowed_date()), "Consultation", "80", True),   # last bookable day
    ("PT-013", str(latest_allowed_date() + timedelta(days=1)), "Consultation", "80", False),  # one day too far
    ("PT-014", str(date.today() + timedelta(days=30)), "Consultation", "80", True),  # next month
    ("PT-006", "2026-08-03", "Rent", "80", False),              # unknown category
    ("", "2026-08-03", "Consultation", "80", False),            # missing patient
    ("PT-008", "2026-08-03", "Consultation", "abc", False),     # cost not a number
]


def show(patient_ref, entry_date, category, cost):
    """Run check_entry on one entry, print the result, return the problems."""
    problems = check_entry(patient_ref, entry_date, category, cost)
    print(f"{patient_ref!r}, {entry_date!r}, {category!r}, {cost!r}")
    if problems:
        for p in problems:
            print("  PROBLEM:", p)
    else:
        print("  OK")
    return problems


def run_samples():
    """Run every sample and compare with what we expect."""
    failures = 0
    for patient_ref, entry_date, category, cost, should_be_ok in SAMPLES:
        problems = show(patient_ref, entry_date, category, cost)
        if (problems == []) != should_be_ok:
            print("  ** UNEXPECTED RESULT **")
            failures += 1
    print(f"\n{len(SAMPLES) - failures}/{len(SAMPLES)} samples behaved as expected.")
    return failures


def main():
    args = sys.argv[1:]
    if args == ["--samples"]:
        sys.exit(1 if run_samples() else 0)
    if len(args) != 4:
        print(__doc__)
        sys.exit(2)
    # Exit code 0 if the entry is fine, 1 if it has problems.
    sys.exit(1 if show(*args) else 0)


if __name__ == "__main__":
    main()
