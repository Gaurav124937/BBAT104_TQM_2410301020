# User Manual — Library Management System

## 1. Starting the Application

Activate the virtual environment and run:

```powershell
python src/main.py
```

The application opens on the Dashboard.

## 2. Dashboard

Use the Dashboard for a high-level view of library activity.

It is intended as the first screen for quickly checking operational status.

## 3. Books

Open **Books** from the sidebar.

Typical operations:

- Add Book
- Search books
- Filter by category / availability
- Select a book
- Edit selected book
- Delete selected book

A book that is currently issued should not be deleted.

## 4. Members

Open **Members**.

Typical operations:

- Add member
- Search members
- Filter by course
- Edit selected member
- Delete selected member

Members with active issued books should not be deleted.

## 5. Issue Book

Open **Issue Book**.

Workflow:

```text
Select available book
      ↓
Select member
      ↓
Enter due date
      ↓
Issue Book
```

The system validates the selected book and member, checks availability and
prevents duplicate active issues.

## 6. Return Book

Open **Return Book**.

Workflow:

```text
Find active issue
      ↓
Select issue
      ↓
Return Book
      ↓
Book availability restored
```

A return cannot be processed twice for the same issue.

## 7. Records

Open **Records**.

The Records module provides:

- Total transactions
- Active transactions
- Overdue transactions
- Returned transactions
- Search by book, member or transaction ID
- Status filtering

Use Records for transaction history review.

## 8. Calendar

Open **Calendar**.

Use month navigation and date selection to review:

- Issue activity
- Due dates
- Return activity

The complete date cell is selectable and the calendar is designed to remain
usable when the application window is resized.

## 9. Appearance and Themes

Open **Settings**.

### Appearance Mode

Choose:

- System
- Light
- Dark

### Theme

Select one of the configured application themes.

After changing the appearance/theme, the application refreshes its UI while
keeping the main application window alive.

## 10. Database Controls

Settings also provides:

- **Initialize Database** — creates/initializes the library database.
- **Reset Database** — permanently clears library records.

Use Reset only when a clean database is intentionally required.

## 11. Troubleshooting

### Application does not start

Confirm the virtual environment is active and run:

```powershell
pip install -r requirements.txt
python src/main.py
```

### Theme selection

Restart the application if you need to confirm the saved appearance/theme
preference is loaded from the runtime settings file.

### Test validation utilities

```powershell
python -m unittest tests/test_validation.py
```
