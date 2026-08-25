# Defect Log — Library Management System

## Purpose

The defect log records observed or test-detected software quality problems in a
consistent format so that defect frequency can later be analyzed using a
checksheet and Pareto analysis.

## Defect Categories

- Validation
- Transaction Accuracy
- Search/Retrieval
- Visibility
- UI/Theme
- Lifecycle / Stability
- Documentation

## Defect Log Template

| Defect ID | Date | Module | Category | Description | Severity | Occurrence | Status | Root Cause | Corrective Action |
|---|---|---|---|---|---:|---:|---|---|---|

## Defect Handling Flow

```text
Observe/Test
    ↓
Record defect
    ↓
Classify category + severity
    ↓
Identify probable cause
    ↓
Apply corrective action
    ↓
Retest
    ↓
Close / Reopen
```

## Status Definitions

| Status | Meaning |
|---|---|
| Open | Defect recorded but not yet corrected |
| In Progress | Corrective action is being worked on |
| Fixed | Correction applied and awaiting/undergoing verification |
| Closed | Retested and confirmed resolved |
| Reopened | Defect returned after a previous fix |

## Severity Scale

| Severity | Meaning |
|---:|---|
| 1 | Cosmetic / negligible |
| 2 | Minor usability impact |
| 3 | Moderate workflow impact |
| 4 | Major workflow impact |
| 5 | Critical failure of a core operation |
