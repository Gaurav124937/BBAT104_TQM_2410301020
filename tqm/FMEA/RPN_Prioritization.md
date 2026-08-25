# RPN Prioritization — Library Management System

RPN is calculated as:

**RPN = Severity × Occurrence × Detection**

## Prioritized Risks

| Rank | Failure Mode | S | O | D | RPN | Risk Class |
|---:|---|---:|---:|---:|---:|---|
| 1 | Records status classification incorrect | 8 | 3 | 5 | 120 | High |
| 2 | Records search misses expected result | 6 | 4 | 5 | 120 | High |
| 3 | Calendar event missing | 8 | 3 | 5 | 120 | High |
| 4 | Incorrect book quantity | 7 | 4 | 4 | 112 | High |
| 5 | Incorrect due date | 7 | 4 | 4 | 112 | High |
| 6 | Incomplete member data | 6 | 4 | 4 | 96 | Medium |
| 7 | Duplicate/conflicting book record | 6 | 3 | 5 | 90 | Medium |
| 8 | Theme change not applied consistently | 5 | 3 | 6 | 90 | Medium |
| 9 | Background UI callback after lifecycle change | 6 | 2 | 7 | 84 | Medium |
| 10 | Dashboard summary mismatch | 8 | 2 | 5 | 80 | Medium |
| 11 | Duplicate active issue | 8 | 3 | 3 | 72 | Medium |
| 12 | Return does not restore availability | 9 | 2 | 4 | 72 | Medium |
| 13 | Issue unavailable book | 9 | 3 | 2 | 54 | Medium |
| 14 | Duplicate return | 8 | 2 | 3 | 48 | Low |

## Risk Action Rule

For the project mitigation plan:

- **RPN ≥ 100:** Immediate mitigation and verification.
- **RPN 70–99:** Mitigation planned and regression testing required.
- **RPN < 70:** Monitor and verify during normal testing.

These thresholds are project management rules for prioritization; they can be
reassessed after defect-log evidence is collected.
