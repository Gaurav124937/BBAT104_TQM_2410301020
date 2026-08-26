# PDCA Cycle — CHECK

## Verification Approach

Compare the improved system behavior against the baseline defect categories and
check whether the targeted controls work as intended.

## Checkpoints

| Area | Verification |
|---|---|
| Validation | Attempt valid, invalid and boundary inputs |
| Transactions | Issue and return complete with correct state |
| Search | Expected records are returned for supported searches |
| Records | Active, Overdue and Returned statuses match transaction data |
| Dashboard | Summary values match database totals |
| Calendar | Issue, Due and Return events appear on correct dates |
| Appearance | Theme/mode changes are reflected across active modules |

## Acceptance Rule

A defect is considered resolved only after the corrected behavior is observed
again in a repeatable verification test.

## Evidence

Record verification outcomes in the defect log and update the checksheet when
a defect is confirmed closed or reopened.
