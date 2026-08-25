# Checksheet — Library Management System Defect Occurrence

## Purpose

This checksheet provides a simple standardized count of quality defects by
category. Counts are used as input for Pareto analysis.

## Defect Occurrence Categories

| Category | Count |
|---|---:|
| Validation | 6 |
| Transaction Accuracy | 5 |
| Search/Retrieval | 4 |
| Visibility | 4 |
| UI/Theme | 3 |
| Lifecycle / Stability | 2 |
| Documentation | 1 |
| **Total** | **25** |

## Recording Rule

For every confirmed defect or test-detected quality issue:

1. Record one occurrence in the defect log.
2. Assign exactly one primary category for the checksheet.
3. Increment the category count.
4. Update the total.
5. Use the resulting frequency table for Pareto analysis.

## Category Interpretation

### Validation — 6
Examples include invalid quantity, incomplete member data, invalid date and
other input-boundary problems.

### Transaction Accuracy — 5
Examples include issue/return state updates, availability consistency or
duplicate transaction concerns.

### Search/Retrieval — 4
Examples include search misses, filtering problems or difficulty locating a
record.

### Visibility — 4
Examples include dashboard/calendar/records data not being visible or matching
the expected stored state.

### UI/Theme — 3
Examples include inconsistent appearance, theme application or layout behavior.

### Lifecycle / Stability — 2
Examples include background UI callbacks or cleanup behavior during application
lifecycle events.

### Documentation — 1
Examples include missing or unclear setup/user guidance discovered during review.
