# SIPOC Process Audit Map — Library Management System

## Project Context

**Baseline System:** Library Management System  
**Quality Goal:** Q03 — Improve Usability  
**Process Area:** Library catalog, member, issue, return, records and usability-support workflow

This SIPOC maps the actual implemented workflow of the project, including the Records module.

## SIPOC Table

| Suppliers | Inputs | Process | Outputs | Customers |
|---|---|---|---|---|
| Librarian / Admin | Book details, quantity, catalog information | 1. Add, update, search and maintain books | Updated catalog and availability information | Librarian |
| Librarian / Admin | Member details | 2. Add, update, search and maintain members | Updated member records | Librarian |
| Librarian / Admin | Available book, valid member, issue date, due date | 3. Issue book | Issue transaction, due date, reduced available quantity | Librarian, Library Member |
| Librarian / Admin | Active issue record, returned book | 4. Return book | Return transaction, updated issue status, increased available quantity | Librarian, Library Member |
| System / SQLite database | Issue and return transactions | 5. Review library records | Unified records history, active/overdue/returned status | Librarian |
| System / SQLite database | Book, member, issue and return data | 6. Search and filter records | Filtered transaction results | Librarian |
| System / SQLite database | Stored transaction dates | 7. Generate usability views | Dashboard statistics and calendar activity | Librarian |
| Application user | Appearance preference | 8. Apply usability settings | Dark/light/system mode and selected application theme | Application User |

## Process Flow

```text
Book & Member Master Data
          ↓
      Issue Book
          ↓
    Active Transaction
       ↙       ↘
   Due/Overdue  Return
       ↓          ↓
     Records ← Return History
          ↓
 Dashboard / Calendar / Search
          ↓
      Library User
```

## Process Boundaries

### Start
The process starts when the librarian enters or updates book/member master data or initiates an issue/return operation.

### End
The process ends when the transaction is stored and the system presents updated catalog, record, dashboard or calendar information.

## Critical Inputs

- Valid book information
- Valid member information
- Book availability
- Valid issue/due dates
- Existing active issue record for returns
- Stored transaction history
- User appearance selection

## Critical Outputs

- Accurate book availability
- Correct issue/return transaction history
- Correct active/overdue/returned status
- Searchable records
- Dashboard statistics
- Calendar activity visibility
- Consistent usability settings

## Key Quality Risks Identified from the Process

| Process Area | Potential Quality Risk |
|---|---|
| Book management | Incorrect quantity or unavailable book information |
| Member management | Incomplete or incorrect member data |
| Issue | Issuing unavailable books or duplicate active issues |
| Return | Duplicate return or incorrect availability update |
| Records | Incorrect transaction status or missing history |
| Search/Filter | User unable to find the expected transaction quickly |
| Dashboard/Calendar | Transaction data not reflected correctly in usability views |
| Appearance | Inconsistent UI state after changing mode/theme |

## Evidence Mapping to the Implemented System

### Books
The Book module maintains catalog data and availability information.

### Members
The Member module maintains member records used by issue/return workflows.

### Issue Book
The issue workflow validates the transaction and updates available quantity.

### Return Book
The return workflow completes the transaction and restores availability.

### Records
The Records module provides a unified transaction history with:
- Total transactions
- Active transactions
- Overdue transactions
- Returned transactions
- Search by book, member, issue ID or return ID
- Status filters

### Dashboard
The Dashboard provides high-level library activity statistics.

### Calendar
The Calendar provides date-based visibility of issue, due and return activity.

### Appearance / Custom Themes
The usability layer provides appearance mode and theme controls.

## TQM Interpretation

The SIPOC shows the library workflow as a connected process rather than isolated CRUD screens:

**Master Data → Issue/Return → Transaction Records → Search/Visibility → Customer-facing usability**

The Records module acts as the transaction-history visibility layer between operational transactions and higher-level dashboard/calendar views.
