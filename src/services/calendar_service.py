from __future__ import annotations

from datetime import date, timedelta

from database.connection import get_connection


def _month_bounds(year: int, month: int) -> tuple[str, str]:
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)
    return start.isoformat(), end.isoformat()


def get_month_events(year: int, month: int) -> dict[int, list[dict]]:
    """Return issue/due/return events grouped by day."""
    start, end = _month_bounds(year, month)

    with get_connection() as connection:
        issue_rows = connection.execute(
            """
            SELECT
                i.issue_id,
                b.title,
                m.name AS member_name,
                i.issue_date
            FROM issues i
            JOIN books b ON b.book_id = i.book_id
            JOIN members m ON m.member_id = i.member_id
            WHERE DATE(i.issue_date) >= DATE(?)
              AND DATE(i.issue_date) < DATE(?)
            ORDER BY DATE(i.issue_date), i.issue_id DESC
            """,
            (start, end),
        ).fetchall()

        due_rows = connection.execute(
            """
            SELECT
                i.issue_id,
                b.title,
                m.name AS member_name,
                i.due_date
            FROM issues i
            JOIN books b ON b.book_id = i.book_id
            JOIN members m ON m.member_id = i.member_id
            WHERE DATE(i.due_date) >= DATE(?)
              AND DATE(i.due_date) < DATE(?)
            ORDER BY DATE(i.due_date), i.issue_id DESC
            """,
            (start, end),
        ).fetchall()

        return_rows = connection.execute(
            """
            SELECT
                r.return_id,
                r.return_date,
                b.title,
                m.name AS member_name
            FROM returns r
            JOIN issues i ON i.issue_id = r.issue_id
            JOIN books b ON b.book_id = i.book_id
            JOIN members m ON m.member_id = i.member_id
            WHERE DATE(r.return_date) >= DATE(?)
              AND DATE(r.return_date) < DATE(?)
            ORDER BY DATE(r.return_date), r.return_id DESC
            """,
            (start, end),
        ).fetchall()

    events: dict[int, list[dict]] = {}

    def add_event(value: str, event_type: str, title: str, details: str) -> None:
        if not value:
            return
        day = int(str(value)[:10][-2:])
        events.setdefault(day, []).append(
            {
                "type": event_type,
                "title": title,
                "details": details,
            }
        )

    for row in issue_rows:
        add_event(
            row["issue_date"],
            "Issue",
            row["title"],
            f'Member: {row["member_name"]} • Issue ID: {row["issue_id"]}',
        )

    for row in due_rows:
        add_event(
            row["due_date"],
            "Due",
            row["title"],
            f'Member: {row["member_name"]} • Issue ID: {row["issue_id"]}',
        )

    for row in return_rows:
        add_event(
            row["return_date"],
            "Return",
            row["title"],
            f'Member: {row["member_name"]} • Return ID: {row["return_id"]}',
        )

    return events


def get_upcoming_due(days: int = 7) -> list[dict]:
    end_date = date.today() + timedelta(days=days)

    with get_connection() as connection:
        return connection.execute(
            """
            SELECT
                i.issue_id,
                b.title,
                m.name AS member_name,
                i.due_date
            FROM issues i
            JOIN books b ON b.book_id = i.book_id
            JOIN members m ON m.member_id = i.member_id
            WHERE i.returned = 0
              AND DATE(i.due_date) BETWEEN DATE('now') AND DATE(?)
            ORDER BY DATE(i.due_date), i.issue_id
            """,
            (end_date.isoformat(),),
        ).fetchall()
