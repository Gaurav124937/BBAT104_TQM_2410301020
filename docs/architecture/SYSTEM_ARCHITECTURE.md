# System Architecture & Flowcharts

## 1. High-Level Architecture

```text
┌───────────────────────────────────────────────┐
│                 Presentation Layer            │
│ Dashboard | Books | Members | Issue | Return │
│ Records | Calendar | Settings                 │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                  Service Layer                 │
│ book_service | member_service | issue_service│
│ return_service | dashboard_service            │
│ calendar_service | theme_manager              │
│ database_admin                                 │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                  Data Layer                    │
│ database.connection | database.schema         │
│ SQLite Database                               │
└───────────────────────────────────────────────┘
```

## 2. Application Startup Flow

```text
Start
  ↓
Initialize SQLite database
  ↓
Load saved appearance/theme
  ↓
Create main LibraryApp window
  ↓
Build sidebar + content area
  ↓
Open Dashboard
  ↓
Ready for user operations
```

## 3. Issue Flow

```text
User selects book + member + due date
                 ↓
          Validate input
                 ↓
         Check book exists
                 ↓
       Check member exists
                 ↓
     Check availability > 0
                 ↓
  Check duplicate active issue
                 ↓
       Create issue record
                 ↓
 Decrease available quantity
                 ↓
          Commit transaction
```

## 4. Return Flow

```text
Select active issue
       ↓
Check issue exists
       ↓
Check not already returned
       ↓
Create return record
       ↓
Mark issue returned
       ↓
Increase available quantity
       ↓
Commit transaction
```

## 5. Quality Improvement Flow

```text
Operational defects
        ↓
Defect Log / Checksheet
        ↓
Pareto Analysis
        ↓
Priority defect categories
        ↓
Fishbone Root Cause
        ↓
FMEA + RPN
        ↓
PDCA improvement actions
        ↓
Verification
        ↓
Standardize / Next cycle
```

## 6. Component Responsibilities

| Component | Responsibility |
|---|---|
| UI | User interaction and presentation |
| Services | Business rules, validation and database operations |
| Database | Persistent storage of books, members and transactions |
| TQM docs | Quality analysis, risk and continuous-improvement artifacts |
