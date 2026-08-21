from database.connection import get_connection

def get_dashboard_stats() -> dict[str, int]:
    with get_connection() as connection:
        return {
            "total_books": int(connection.execute(
                "SELECT COALESCE(SUM(quantity), 0) AS value FROM books"
            ).fetchone()["value"]),
            "available_books": int(connection.execute(
                "SELECT COALESCE(SUM(available_quantity), 0) AS value FROM books"
            ).fetchone()["value"]),
            "issued_books": int(connection.execute(
                "SELECT COUNT(*) AS value FROM issues WHERE returned = 0"
            ).fetchone()["value"]),
            "total_members": int(connection.execute(
                "SELECT COUNT(*) AS value FROM members"
            ).fetchone()["value"]),
            "overdue_books": int(connection.execute(
                """
                SELECT COUNT(*) AS value
                FROM issues
                WHERE returned = 0 AND DATE(due_date) < DATE('now')
                """
            ).fetchone()["value"]),
            "returned_today": int(connection.execute(
                """
                SELECT COUNT(*) AS value
                FROM returns
                WHERE DATE(return_date) = DATE('now')
                """
            ).fetchone()["value"]),
        }

def get_recent_issues(limit: int = 8):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT i.issue_id, b.title, m.name AS member_name,
                   i.issue_date, i.due_date,
                   CASE
                     WHEN i.returned = 1 THEN 'Returned'
                     WHEN DATE(i.due_date) < DATE('now') THEN 'Overdue'
                     ELSE 'Active'
                   END AS status
            FROM issues i
            JOIN books b ON b.book_id = i.book_id
            JOIN members m ON m.member_id = i.member_id
            ORDER BY i.issue_id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

def get_recent_returns(limit: int = 8):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT r.return_id, b.title, m.name AS member_name, r.return_date
            FROM returns r
            JOIN issues i ON i.issue_id = r.issue_id
            JOIN books b ON b.book_id = i.book_id
            JOIN members m ON m.member_id = i.member_id
            ORDER BY r.return_id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
