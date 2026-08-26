# Fishbone Root-Cause Analysis — Library Management System

## Quality Problem

The Pareto analysis identified four priority defect categories:

- Validation
- Transaction Accuracy
- Search/Retrieval
- Visibility

The Fishbone analysis groups likely root causes under the project's required
Ishikawa dimensions: **People, Process, Software Code and Infrastructure**.

## Central Effect

```text
                    LIBRARY SOFTWARE
                 QUALITY / USABILITY
                      DEFECTS
                         ↑
        ┌──────────┬─────┼─────┬──────────┐
        │          │     │     │          │
      People    Process  Code  Infrastructure
```

## People

Potential causes:

- User enters incomplete or incorrect information.
- Librarian may not immediately notice an overdue or incorrect record.
- Different users may follow slightly different data-entry practices.
- Users may not know the intended search/filter behavior.
- Appearance changes may be used during an active workflow without checking the
  resulting screen state.

## Process

Potential causes:

- Validation rules are not applied at every relevant input boundary.
- Issue and return steps depend on correct transaction sequencing.
- Record status depends on stored issue/return and due-date information.
- Defect verification may not cover every search/filter combination.
- Calendar and dashboard visibility depend on transaction data being stored
  correctly.
- Regression testing may not initially cover every usability change.

## Software Code

Potential causes:

- Edge cases in validation logic.
- Incorrect or incomplete date handling.
- Query filtering conditions that omit expected records.
- Mismatch between stored transaction state and displayed status.
- UI state not being refreshed consistently after theme changes.
- Widget lifecycle callbacks occurring while UI controls are being rebuilt.
- Different modules using different presentation or refresh logic.

## Infrastructure

Potential causes:

- Python/CustomTkinter runtime and widget lifecycle behavior.
- Local SQLite data state and schema.
- Virtual-environment package/version differences.
- Operating-system GUI event scheduling.
- Runtime cache/bytecode state during development.
- Window scaling/DPI behavior.

## Root-Cause Priorities

| Cause Area | Priority | Reason |
|---|---|---|
| Software Code | High | Directly affects validation, queries, status logic and UI refresh |
| Process | High | Weak verification steps can allow defects through despite correct code |
| People | Medium | User entry and workflow behavior can generate or hide issues |
| Infrastructure | Medium | Runtime/version/lifecycle behavior can produce non-business defects |

## Recommended Root-Cause Checks

1. Verify each defect against the smallest reproducible workflow.
2. Compare the displayed result with the SQLite source record.
3. Add regression tests for every corrected validation/query/date rule.
4. Repeat the same workflow after theme and appearance changes.
5. Record whether the problem originated in input, business logic, query,
   presentation or runtime lifecycle.

## TQM Interpretation

The Fishbone does not assume that every observed defect has one cause.
Instead, it separates potential causes by category so corrective actions can
be targeted and then verified through PDCA.
