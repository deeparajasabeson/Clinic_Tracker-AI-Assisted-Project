# Clinic Appointment and Expense Tracker

Work in progress. Only `check_entry` is built so far; everything else is an
empty outline. No UI: parts are plain Python functions to be called from code
or tests.

## Status

| File | Purpose | Status |
|---|---|---|
| validation.py | Input checks. `check_entry` and `latest_allowed_date` are built | Partly built |
| try_check_entry.py | Command-line tester for `check_entry` | Built |
| RULES.md | Business rules, tricky cases, and which code/test covers each | Written |
| models.py | Appointment and Expense records | Outline only |
| storage.py | Save/load JSON files in data/ | Outline only |
| appointments.py | Book, list, cancel, reschedule, double-booking check | Outline only |
| expenses.py | Add, list, filter, totals by category/month | Outline only |
| reports.py | Weekly appointment and monthly expense summaries | Outline only |
| data/ | JSON files created at runtime | Empty |

In validation.py, `validate_date`, `validate_datetime`, `validate_name` and
`validate_amount` are still empty placeholders. `check_entry` does not use them.

## check_entry

`check_entry(patient_ref, entry_date, category, cost)` returns a list of
problem messages. An empty list means the entry is fine.

- Date: `YYYY-MM-DD`, from 2000-01-01 up to today + 3 months.
- Category: Consultation, Diagnostics, Procedure, Follow-up or Pharmacy
  (capital letters ignored).
- Cost: a number; zero is allowed, negative is refused.

Full list of rules and open assumptions: see [RULES.md](RULES.md).

## Try it

Run from this folder:

```
python try_check_entry.py PT-001 2026-08-03 Consultation 120.00
python try_check_entry.py --samples
```

## Build order
1. models.py + storage.py
2. validation.py (finish the placeholders, or remove them)
3. appointments.py
4. expenses.py
5. reports.py
