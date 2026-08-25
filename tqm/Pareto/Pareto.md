# Pareto Analysis — Library Management System

## Purpose

Pareto analysis identifies the small number of defect categories contributing
the largest share of observed defects. This analysis uses the counts recorded
in the project checksheet.

## Input Data

Total recorded defect occurrences: **25**

| Category | Frequency |
|---|---:|
| Validation | 6 |
| Transaction Accuracy | 5 |
| Search/Retrieval | 4 |
| Visibility | 4 |
| UI/Theme | 3 |
| Lifecycle / Stability | 2 |
| Documentation | 1 |

## Pareto Table

| Rank | Category | Frequency | Percentage | Cumulative Percentage |
|---:|---|---:|---:|---:|
| 1 | Validation | 6 | 24.0% | 24.0% |
| 2 | Transaction Accuracy | 5 | 20.0% | 44.0% |
| 3 | Search/Retrieval | 4 | 16.0% | 60.0% |
| 4 | Visibility | 4 | 16.0% | 76.0% |
| 5 | UI/Theme | 3 | 12.0% | 88.0% |
| 6 | Lifecycle / Stability | 2 | 8.0% | 96.0% |
| 7 | Documentation | 1 | 4.0% | 100.0% |

## 80/20 Interpretation

The first four categories are:

1. Validation
2. Transaction Accuracy
3. Search/Retrieval
4. Visibility

Together they account for:

**6 + 5 + 4 + 4 = 19 defects**

**19 / 25 = 76.0%**

Therefore, the first four categories represent approximately **76% of the
recorded defect occurrences** and are the primary areas for corrective-action
focus.

The remaining categories account for approximately 24% of the observations.

## Recommended Improvement Focus

Based on the Pareto result, improvement effort should first concentrate on:

- Validation quality and input-boundary controls.
- Issue/return transaction accuracy.
- Search and retrieval reliability.
- Visibility across Records, Dashboard and Calendar.

This prioritization can be used as an input to Fishbone root-cause analysis and
PDCA corrective actions.

## Traceability

Source of frequencies:

`tqm/Defect_Control/Checksheet.md`

The frequencies are carried forward from the defect-control milestone rather
than invented independently for this analysis.
