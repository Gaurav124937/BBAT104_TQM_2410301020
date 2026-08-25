# CTQ Tree — Library Management System

## Project Context

**Baseline System:** Library Management System  
**Quality Goal:** Q03 — Improve Usability

The CTQ (Critical to Quality) tree converts the main user need — **an easy, reliable and efficient library operation experience** — into measurable quality characteristics for the implemented application.

## CTQ Tree

```text
                     CUSTOMER NEED
          Easy and Reliable Library Operation
                         |
       +-----------------+------------------+
       |                 |                  |
   Fast Retrieval    Transaction        Clear Visibility
                     Accuracy
       |                 |                  |
   +---+---+        +----+----+        +----+----+
   |       |        |         |        |         |
Search   Navigation Issue/   Return  Records   Dashboard/
Filters            Return    Accuracy          Calendar
                   Accuracy
       |
       +----------------------+
       |
   Usable Interface
       |
   +---+---+
   |       |
Appearance  Consistency
Mode/Theme across modules
```

## CTQ Matrix

| Customer Need | Critical to Quality | Measurable Requirement | Application Evidence |
|---|---|---|---|
| Easy library operation | Fast retrieval | User can search/filter records without manually scanning all entries | Books, Members, Records search/filter |
| Easy library operation | Quick navigation | Main modules are reachable from the common sidebar navigation | Dashboard, Books, Members, Issue, Return, Records, Calendar, Settings |
| Reliable transactions | Issue accuracy | System should prevent issuing an unavailable book and prevent duplicate active issue | Issue workflow |
| Reliable transactions | Return accuracy | Returned transactions should update issue status and book availability correctly | Return workflow |
| Clear visibility | Record visibility | Issue/return history should be available in a unified records screen | Records module |
| Clear visibility | Activity visibility | Issue, due and return activity should be visible by date | Calendar module |
| Clear visibility | Operational overview | Current library activity should be summarized for the operator | Dashboard Overview |
| Usable interface | Appearance control | User can select System, Light or Dark appearance | Settings |
| Usable interface | Theme choice | User can select an application theme | Custom Themes |
| Consistent interface | Cross-module consistency | Appearance/theme changes should apply across the application | Sidebar + module views |

## Proposed CTQ Measures

The following measures can be used later in defect logs, checksheets and continuous-improvement reviews.

| CTQ | Suggested Measure | Target Direction |
|---|---|---|
| Search retrieval | Time to locate a required book/member/record | Lower is better |
| Navigation | Number of navigation steps to reach a core module | Lower is better |
| Issue accuracy | Invalid issue transactions accepted | Zero |
| Return accuracy | Incorrect return transactions accepted | Zero |
| Record completeness | Transactions missing from Records | Zero |
| Calendar visibility | Transactions missing from date-based calendar | Zero |
| Dashboard correctness | Dashboard values inconsistent with database | Zero |
| Theme consistency | Modules remaining in old appearance after theme change | Zero |
| Usability errors | User-facing interface errors during normal workflow | Lower is better |

## CTQ Priority for Q03

For the assigned usability goal, the priority order is:

1. **Fast retrieval** — search/filter reduces effort in finding information.
2. **Clear visibility** — dashboard, records and calendar make status easier to understand.
3. **Usable interface** — appearance modes and custom themes improve user comfort and control.
4. **Navigation** — common navigation keeps major workflows easy to access.
5. **Transaction accuracy** — usability depends on correct issue/return feedback and status.

## Link to TQM

The CTQ tree provides measurable quality characteristics that can later be connected to:

**CTQ → Defect Log → Checksheet → Pareto Analysis → Root Cause/Fishbone → PDCA**

This keeps the TQM analysis tied to measurable software quality rather than only visual design.
