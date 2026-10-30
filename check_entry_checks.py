"""Plain checks for check_entry. No test framework, just printed lines.

Run:
    python check_entry_checks.py
"""

import sys
from datetime import date, datetime, timedelta

from validation import check_entry, latest_allowed_date

# A date that is always valid (in the past, after 2000-01-01).
GOOD_DATE = "2026-08-03"

# Dates that move with the calendar, for the boundary checks.
TODAY = date.today()
LATEST = latest_allowed_date()

# Each check is: (name, entry values, expected)
# expected is one of:
#   "OK"                  no problems
#   "some text"           exactly one problem, containing that text
#   ["text1", "text2"]    several problems, in this order
CHECKS = [
    # --- Cost ---
    ("Good entry",
     ("PT-001", GOOD_DATE, "Consultation", "120.00"), "OK"),
    ("Cost exactly zero",
     ("PT-001", GOOD_DATE, "Consultation", "0"), "OK"),
    ("Cost minus 0.01 (just below zero)",
     ("PT-001", GOOD_DATE, "Consultation", "-0.01"), "Cost cannot be negative."),
    ("Clearly negative cost",
     ("PT-001", GOOD_DATE, "Consultation", "-50"), "Cost cannot be negative."),

    # --- Category ---
    ("Unknown category",
     ("PT-001", GOOD_DATE, "Rent", "120"), "Category must be one of"),
    ("Empty category",
     ("PT-001", GOOD_DATE, "", "120"), "Category is required."),

    # --- Category variations ---
    ("Category all lowercase",
     ("PT-001", GOOD_DATE, "consultation", "120"), "OK"),
    ("Category all capitals",
     ("PT-001", GOOD_DATE, "PHARMACY", "120"), "OK"),
    ("Category with spaces around it",
     ("PT-001", GOOD_DATE, "  Diagnostics  ", "120"), "OK"),
    ("Category Follow-up in lowercase",
     ("PT-001", GOOD_DATE, "follow-up", "120"), "OK"),
    ("Category Follow up (space, no hyphen)",
     ("PT-001", GOOD_DATE, "Follow up", "120"), "Category must be one of"),
    ("Category Followup (no hyphen)",
     ("PT-001", GOOD_DATE, "Followup", "120"), "Category must be one of"),
    ("Category plural (Procedures)",
     ("PT-001", GOOD_DATE, "Procedures", "120"), "Category must be one of"),

    # --- Patient ID format ---
    # Current rule: any non-blank text is accepted. No PT-000 pattern is enforced.
    ("Patient ID in the example format",
     ("PT-001", GOOD_DATE, "Consultation", "120"), "OK"),
    ("Patient ID empty",
     ("", GOOD_DATE, "Consultation", "120"), "Patient reference is required."),
    ("Patient ID spaces only",
     ("   ", GOOD_DATE, "Consultation", "120"), "Patient reference is required."),
    ("Patient ID missing (None)",
     (None, GOOD_DATE, "Consultation", "120"), "Patient reference is required."),
    ("Patient ID in a different format (accepted: no pattern enforced)",
     ("abc123", GOOD_DATE, "Consultation", "120"), "OK"),
    ("Patient ID lowercase pt-001 (accepted: no pattern enforced)",
     ("pt-001", GOOD_DATE, "Consultation", "120"), "OK"),

    # --- Edge cases: cost ---
    ("Edge: cost 0.00 written with decimals",
     ("PT-001", GOOD_DATE, "Consultation", "0.00"), "OK"),
    ("Edge: cost minus zero (-0)",
     ("PT-001", GOOD_DATE, "Consultation", "-0"), "OK"),
    ("Edge: cost -0.001 (tiny negative)",
     ("PT-001", GOOD_DATE, "Consultation", "-0.001"), "Cost cannot be negative."),
    ("Edge: cost as a real number, not text (0)",
     ("PT-001", GOOD_DATE, "Consultation", 0), "OK"),
    ("Edge: cost as a real negative number (-1)",
     ("PT-001", GOOD_DATE, "Consultation", -1), "Cost cannot be negative."),
    ("Edge: cost with spaces around it",
     ("PT-001", GOOD_DATE, "Consultation", "  120  "), "OK"),
    ("Edge: very large cost (no upper limit)",
     ("PT-001", GOOD_DATE, "Consultation", "99999999.99"), "OK"),
    ("Edge: cost with three decimals (no decimal rule)",
     ("PT-001", GOOD_DATE, "Consultation", "1.234"), "OK"),
    ("Edge: cost is None",
     ("PT-001", GOOD_DATE, "Consultation", None), "Cost must be a number."),
    ("Edge: cost is empty text",
     ("PT-001", GOOD_DATE, "Consultation", ""), "Cost must be a number."),
    ("Edge: cost is words",
     ("PT-001", GOOD_DATE, "Consultation", "abc"), "Cost must be a number."),
    ("Edge: cost with currency symbol ($120)",
     ("PT-001", GOOD_DATE, "Consultation", "$120"), "Cost must be a number."),
    ("Edge: cost with thousands comma (1,200)",
     ("PT-001", GOOD_DATE, "Consultation", "1,200"), "Cost must be a number."),
    ("Edge: cost is NaN (not a number)",
     ("PT-001", GOOD_DATE, "Consultation", "nan"), "Cost must be a number."),
    ("Edge: cost is infinity",
     ("PT-001", GOOD_DATE, "Consultation", "inf"), "Cost must be a number."),

    # --- Edge cases: dates ---
    ("Edge: earliest allowed date (2000-01-01)",
     ("PT-001", "2000-01-01", "Consultation", "120"), "OK"),
    ("Edge: one day before earliest (1999-12-31)",
     ("PT-001", "1999-12-31", "Consultation", "120"), "Date must be between"),
    ("Edge: today",
     ("PT-001", str(TODAY), "Consultation", "120"), "OK"),
    ("Edge: last bookable day (today + 3 months)",
     ("PT-001", str(LATEST), "Consultation", "120"), "OK"),
    ("Edge: one day after last bookable day",
     ("PT-001", str(LATEST + timedelta(days=1)), "Consultation", "120"), "Date must be between"),
    ("Edge: leap day that exists (2024-02-29)",
     ("PT-001", "2024-02-29", "Consultation", "120"), "OK"),
    ("Edge: leap day that does not exist (2025-02-29)",
     ("PT-001", "2025-02-29", "Consultation", "120"), "Date must be a real date"),
    ("Edge: 31st of a 30-day month (2026-04-31)",
     ("PT-001", "2026-04-31", "Consultation", "120"), "Date must be a real date"),
    ("Edge: day/month/year format (03/08/2026)",
     ("PT-001", "03/08/2026", "Consultation", "120"), "Date must be a real date"),
    ("Edge: date without leading zeros (2026-8-3)",
     ("PT-001", "2026-8-3", "Consultation", "120"), "OK"),
    ("Edge: date with a space after it",
     ("PT-001", "2026-08-03 ", "Consultation", "120"), "Date must be a real date"),
    ("Edge: date is empty text",
     ("PT-001", "", "Consultation", "120"), "Date must be a real date"),
    ("Edge: date is None",
     ("PT-001", None, "Consultation", "120"), "Date must be a real date"),
    ("Edge: date given as a real date object",
     ("PT-001", date(2026, 8, 3), "Consultation", "120"), "OK"),
    ("Edge: date given as a date-and-time object",
     ("PT-001", datetime(2026, 8, 3, 14, 30), "Consultation", "120"), "OK"),
    ("Edge: date object too far ahead",
     ("PT-001", LATEST + timedelta(days=1), "Consultation", "120"), "Date must be between"),

    # --- Edge cases: several problems at once ---
    ("Edge: everything wrong at once (4 problems)",
     ("", "2026-13-40", "Rent", "abc"),
     ["Patient reference is required.", "Date must be a real date",
      "Category must be one of", "Cost must be a number."]),
    ("Edge: date too far ahead and negative cost (2 problems)",
     ("PT-001", str(LATEST + timedelta(days=1)), "Consultation", "-5"),
     ["Date must be between", "Cost cannot be negative."]),
    ("Edge: empty everything (None, None, None, None)",
     (None, None, None, None),
     ["Patient reference is required.", "Date must be a real date",
      "Category is required.", "Cost must be a number."]),
]


def run_check(name, values, expected):
    """Run one check, print the result line, return True if it passed."""
    got = check_entry(*values)

    if expected == "OK":
        passed = got == []
        expected_text = "[] (no problems)"
    elif isinstance(expected, list):
        # Passed if there is one problem per expected text, in the same order.
        passed = len(got) == len(expected) and all(
            text in problem for text, problem in zip(expected, got)
        )
        expected_text = f"{len(expected)} problems containing: {expected}"
    else:
        # Passed if exactly one problem is reported and it contains the text.
        passed = len(got) == 1 and expected in got[0]
        expected_text = f"one problem containing: {expected!r}"

    print(f"{name}")
    print(f"  expected: {expected_text}")
    print(f"  got:      {got}")
    print(f"  {'PASS' if passed else 'FAIL'}")
    return passed


def main():
    failures = 0
    for name, values, expected in CHECKS:
        if not run_check(name, values, expected):
            failures += 1
    print()
    print(f"{len(CHECKS) - failures} of {len(CHECKS)} checks passed.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
