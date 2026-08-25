# FMEA Matrix — Library Management System

## Project Context

Baseline System: Library Management System  
Quality Goal: Q03 — Improve Usability

FMEA is used to identify process/software failure modes, assess Severity (S),
Occurrence (O), and Detection (D), calculate Risk Priority Number (RPN),
and define mitigation actions.

**RPN = Severity × Occurrence × Detection**

## Rating Scale

### Severity (S)

| Score | Meaning |
|---|---|
| 1 | Negligible impact on the user/process |
| 2–3 | Minor inconvenience |
| 4–6 | Moderate operational impact |
| 7–8 | Major operational impact |
| 9–10 | Critical impact / major loss of process integrity |

### Occurrence (O)

| Score | Meaning |
|---|---|
| 1 | Rare |
| 2–3 | Uncommon |
| 4–6 | Occasional |
| 7–8 | Frequent |
| 9–10 | Very frequent |

### Detection (D)

| Score | Meaning |
|---|---|
| 1 | Almost certain to be detected before impact |
| 2–3 | High chance of detection |
| 4–6 | Moderate detection |
| 7–8 | Low detection |
| 9–10 | Very difficult to detect |

## FMEA Matrix

| Process | Failure Mode | Effect | S | O | D | RPN | Current Control | Recommended Mitigation |
|---|---|---|---:|---:|---:|---:|---|---|
| Book Management | Incorrect quantity entered | Availability becomes inaccurate | 7 | 4 | 4 | 112 | Input validation | Strict numeric/range validation and clear validation feedback |
| Book Management | Duplicate/conflicting book record | Search/catalog confusion | 6 | 3 | 5 | 90 | Book management controls | Strengthen uniqueness checks and duplicate prevention |
| Member Management | Incomplete member data | Member cannot be reliably identified | 6 | 4 | 4 | 96 | Required-field checks | Stronger validation and field-level feedback |
| Issue Book | Issue unavailable book | Wrong inventory state / failed service | 9 | 3 | 2 | 54 | Availability validation | Keep availability check immediately before issue transaction |
| Issue Book | Duplicate active issue | Multiple active records for same book/member | 8 | 3 | 3 | 72 | Duplicate issue validation | Add explicit duplicate-warning message and test case |
| Issue Book | Incorrect due date | Overdue calculation becomes inaccurate | 7 | 4 | 4 | 112 | Due-date validation | Enforce valid date rule and test boundary dates |
| Return Book | Duplicate return | Transaction history becomes inconsistent | 8 | 2 | 3 | 48 | Return validation | Keep one-return-per-issue rule and add regression test |
| Return Book | Availability not restored | Book remains incorrectly unavailable | 9 | 2 | 4 | 72 | Return transaction update | Verify issue status and available quantity atomically |
| Records | Incorrect status classification | Librarian may act on wrong transaction state | 8 | 3 | 5 | 120 | Status calculated from issue/return data | Add automated status tests for Active/Overdue/Returned |
| Records | Search misses expected record | Retrieval effort increases | 6 | 4 | 5 | 120 | Search/filter interface | Add search test matrix for title/member/IDs and partial matches |
| Dashboard | Summary differs from transaction data | Operator receives misleading overview | 8 | 2 | 5 | 80 | Database-derived statistics | Add dashboard-vs-database verification test |
| Calendar | Issue/Due/Return event missing from date | User misses important activity | 8 | 3 | 5 | 120 | Database-driven calendar queries | Add date-format and event-presence regression tests |
| Appearance | Theme change not applied to all modules | Inconsistent user interface | 5 | 3 | 6 | 90 | Theme manager + UI refresh | Verify sidebar and all module views after every theme change |
| Application Lifecycle | Background UI callback after window lifecycle change | Terminal error / unstable shutdown behavior | 6 | 2 | 7 | 84 | Current Tk lifecycle handling | Avoid root destruction during theme refresh; add clean shutdown test |

## Risk Prioritization

High-priority items are those with the largest RPN values and therefore deserve
earlier mitigation.

### Highest Current Risks

| Failure Mode | RPN | Priority |
|---|---:|---|
| Records status classification incorrect | 120 | High |
| Records search misses expected result | 120 | High |
| Calendar event missing | 120 | High |
| Incorrect book quantity | 112 | High |
| Incorrect due date | 112 | High |
| Incomplete member data | 96 | Medium |
| Duplicate/conflicting book record | 90 | Medium |
| Theme inconsistency | 90 | Medium |

## FMEA Mitigation Principle

The preferred mitigation is to reduce risk through prevention and early
detection:

**Prevent incorrect input → validate transaction → verify stored state →
expose clear status → regression test critical workflows.**

The FMEA should be revisited after defect and checksheet data are collected so
that Occurrence and Detection scores can be adjusted using project evidence.
