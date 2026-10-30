# Business rules and tricky cases for `check_entry`

All rules live in `validation.py`. "Sample" means a row in `SAMPLES` in
`try_check_entry.py` (run with `python try_check_entry.py --samples`).
"Checked by hand" means I ran it once in a terminal but it is **not** in the
sample list yet, so it would not be caught if it broke later.

Source: **You** = stated by you, **Agreed** = proposed and accepted after
you reviewed it, **Assumed** = my choice, not yet confirmed by you.

## Output

| Rule | Source | Code |
|---|---|---|
| Returns a list of problem messages; empty list = entry is fine | You | `check_entry`, `problems` list and `return` (lines 31, 70) |
| All problems are reported together, not just the first | Assumed | the separate `if` blocks in `check_entry` |

## Patient reference

| Rule | Source | Code | Tested by |
|---|---|---|---|
| Must not be empty or only spaces | Assumed | lines 33-35 | Sample `""` (missing patient). Spaces-only: not tested |
| No format enforced (`PT-001` and `abc` both pass) | Assumed | same lines (no pattern check) | Not tested |

## Date

| Rule | Source | Code | Tested by |
|---|---|---|---|
| Format is `YYYY-MM-DD`; `03/08/2026` is refused | Assumed | line 45 | Not tested |
| Impossible dates such as `2026-13-40` are refused | You (example) | lines 44-47 | Sample PT-005 |
| A real date object is accepted as well as text | Assumed | lines 39-42 | Not tested |
| Earliest date is 2000-01-01 | Agreed (after you found 18?? and 10?? accepted) | `MIN_DATE`, line 51 | Samples PT-009, PT-010. The boundary day itself (2000-01-01 ok, 1999-12-31 refused): checked by hand |
| Latest date is today + 3 months (clinic books at most 3 months ahead) | You | `MAX_MONTHS_AHEAD`, `latest_allowed_date`, line 51 | Samples PT-011, PT-012 (last day ok), PT-013 (one day too far), PT-014 (inside window) |
| "3 months" means calendar months, not 90 days | Assumed | `latest_allowed_date` lines 20-22 | Checked by hand (see next row) |
| If the day does not exist in the target month, use the month's last day (30 Nov -> 28 Feb) | Assumed | line 24 | Checked by hand: 29 Oct 2026->29 Jan 2027, 30 Nov 2026->28 Feb 2027, 31 Dec 2026->31 Mar 2027, 30 Nov 2027->29 Feb 2028 (leap year). Not in samples |
| The year rolls over correctly when the window crosses New Year | Assumed | lines 21-22 | Checked by hand (31 Dec case above). Not in samples |
| Past dates are accepted back to 2000 (no "not in the past" rule) | Assumed | line 51 has no lower limit other than `MIN_DATE` | Sample PT-001 and others use past dates |
| The cutoff moves every day because it is based on today | Consequence | `date.today()` line 18 | Samples build their dates from `latest_allowed_date()` so they stay valid |

## Category

| Rule | Source | Code | Tested by |
|---|---|---|---|
| Only Consultation, Diagnostics, Procedure, Follow-up, Pharmacy are valid | You | `VALID_CATEGORIES`, lines 57-58 | Sample PT-006 (`Rent` refused) |
| Capital letters and surrounding spaces are ignored (`follow-up`, ` Pharmacy `) | Assumed | line 57 (`.strip().lower()`) | Sample PT-003 (`follow-up`). Extra spaces: not tested |
| Empty category gets its own message ("Category is required.") | Assumed | lines 55-56 | Not tested |

## Cost

| Rule | Source | Code | Tested by |
|---|---|---|---|
| Negative cost is refused | You | lines 67-68 | Sample PT-004 |
| Zero cost is allowed | You | line 67 (`>= 0`) | Sample PT-002 |
| Cost typed as text (`"120.00"`) is accepted | Assumed | line 62 (`float`) | Sample PT-001 |
| Non-numbers such as `abc` or nothing at all are refused | Assumed | lines 63-64 | Sample PT-008. `None`: not tested |
| NaN ("not a number") and infinity are refused with "Cost must be a number." (found by the edge-case checks; infinity used to be accepted, NaN had the wrong message) | Assumed | `math.isfinite` check in `check_entry` | `check_entry_checks.py`: "cost is NaN", "cost is infinity" |
| Currency symbols (`$120`) and thousands commas (`1,200`) are refused | Assumed | line 62 | Not tested |
| No upper limit and no decimal-place rule (`1.234` passes) | Assumed | no check exists | Not tested |

## Not built yet

`validate_date`, `validate_datetime`, `validate_name` and `validate_amount`
in `validation.py` are empty placeholders from the first outline. No rule
above depends on them.

## Suggested next step

Add the "Checked by hand" and "Not tested" rows to `SAMPLES`, especially
the date boundary, the month-end clamp, NaN and spaces-only values. Those are
the rules most likely to break silently.
