# FMEA Mitigation & Action Plan

| ID | Risk / Failure Mode | Action | Verification | Status |
|---|---|---|---|---|
| M01 | Records status classification | Add explicit tests for Active, Overdue and Returned states | Run records test matrix | Planned |
| M02 | Records search misses result | Test title/member/issue ID/return ID and partial matches | Search regression tests | Planned |
| M03 | Calendar event missing | Verify issue, due and return events across date formats | Calendar date regression tests | Planned |
| M04 | Incorrect book quantity | Enforce positive integer quantity and availability consistency | Book validation tests | Planned |
| M05 | Incorrect due date | Validate due date and boundary conditions | Issue date test cases | Planned |
| M06 | Incomplete member data | Validate required fields with clear user messages | Member validation tests | Planned |
| M07 | Duplicate book record | Add duplicate/uniqueness checks where appropriate | Duplicate-entry test | Planned |
| M08 | Theme inconsistency | Rebuild active application views without destroying the root | Theme regression test | Planned |
| M09 | UI lifecycle callback | Avoid destroying the root during theme refresh and test clean shutdown | Start/change-theme/close test | Planned |
| M10 | Dashboard mismatch | Compare dashboard values with direct database queries | Dashboard verification test | Planned |
| M11 | Duplicate active issue | Preserve duplicate-issue validation | Issue regression tests | Planned |
| M12 | Return availability mismatch | Verify returned issue status and available quantity after each return | Return regression test | Planned |

## Action Priority

The first mitigation wave should focus on the highest RPN risks:

1. Records status classification
2. Records search
3. Calendar event visibility
4. Book quantity validation
5. Due-date validation

The second wave should address medium-risk usability and lifecycle issues.
