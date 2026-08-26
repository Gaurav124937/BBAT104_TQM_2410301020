# BBAT104 TQM — Library Management System

## Project Overview

This project is a Python desktop Library Management System developed for the
BBAT104 Fundamentals of TQM course project.

**Baseline System:** Library Management System  
**Quality Goal:** Q03 — Improve Usability

The implementation focuses on core library operations and usability features:
Dashboard Overview, Search/Filter support, Calendar, Dark Mode and Custom
Themes. A Records module was also added to provide unified transaction history.

## Core Modules

- **Dashboard** — operational library overview and activity statistics.
- **Books** — add, view, edit, delete, search and filter books.
- **Members** — add, view, edit, delete, search and filter members.
- **Issue Book** — issue available books to valid members and assign due dates.
- **Return Book** — process book returns and restore availability.
- **Records** — unified issue/return history with status filters.
- **Calendar** — date-based issue, due and return visibility.
- **Settings** — appearance mode, theme selection and database controls.

## Technology Stack

- Python 3.x
- CustomTkinter
- SQLite
- Pandas
- Matplotlib
- Seaborn

## Project Structure

```text
src/
├── database/
├── models/
├── services/
├── ui/
└── utils/

tests/
tqm/
docs/
requirements.txt
```

## Run the Project

### 1. Create / activate the virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run

```powershell
python src/main.py
```

## Quality Goal Q03

The project implements the five suggested usability features listed for Q03:

1. Dashboard Overview
2. Search Filters
3. Calendar
4. Dark Mode
5. Custom Themes

## TQM Deliverables

The repository contains TQM analysis artifacts including:

- SIPOC Process Audit Map
- CTQ Tree
- FMEA Matrix
- RPN Prioritization
- Mitigation Action Plan
- Defect Log
- Checksheet
- Pareto Analysis
- Fishbone Root Cause Analysis
- PDCA Cycle

## Quality Approach

The project follows a continuous-improvement flow:

```text
Measure defects
      ↓
Prioritize with Pareto
      ↓
Find causes with Fishbone
      ↓
Assess risk with FMEA
      ↓
Plan improvements with PDCA
      ↓
Verify and standardize
```

## Repository

Keep `.venv/`, Python cache files and runtime preference files out of source
control using `.gitignore`.
