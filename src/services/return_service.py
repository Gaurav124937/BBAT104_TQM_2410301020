from datetime import date
from database.connection import get_connection


def return_book(issue_id: int) -> None:
    with get_connection() as connection:
        issue = connection.execute(
            """
            SELECT book_id, returned
            FROM issues
            WHERE issue_id = ?
            """,
            (issue_id,),
        ).fetchone()

        if issue is None:
            raise ValueError("Issue record not found.")

        if issue["returned"]:
            raise ValueError("This book has already been returned.")

        connection.execute(
            """
            INSERT INTO returns (issue_id, return_date)
            VALUES (?, ?)
            """,
            (issue_id, date.today().isoformat()),
        )

        connection.execute(
            """
            UPDATE issues
            SET returned = 1
            WHERE issue_id = ?
            """,
            (issue_id,),
        )

        connection.execute(
            """
            UPDATE books
            SET available_quantity = available_quantity + 1
            WHERE book_id = ?
            """,
            (issue["book_id"],),
        )

        connection.commit()


def list_returned_books():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT
                r.return_id,
                r.issue_id,
                b.title,
                m.name AS member_name,
                i.issue_date,
                i.due_date,
                r.return_date
            FROM returns r
            JOIN issues i ON i.issue_id = r.issue_id
            JOIN books b ON b.book_id = i.book_id
            JOIN members m ON m.member_id = i.member_id
            ORDER BY DATE(r.return_date) DESC, r.return_id DESC
            """
        ).fetchall()


def search_returned_books(query: str = ""):
    query = query.strip()

    sql = """
        SELECT
            r.return_id,
            r.issue_id,
            b.title,
            m.name AS member_name,
            i.issue_date,
            i.due_date,
            r.return_date
        FROM returns r
        JOIN issues i ON i.issue_id = r.issue_id
        JOIN books b ON b.book_id = i.book_id
        JOIN members m ON m.member_id = i.member_id
        WHERE 1 = 1
    """
    params = []

    if query:
        like_query = f"%{query}%"
        sql += """
            AND (
                b.title LIKE ?
                OR m.name LIKE ?
                OR CAST(r.issue_id AS TEXT) LIKE ?
                OR CAST(r.return_id AS TEXT) LIKE ?
            )
        """
        params.extend([like_query, like_query, like_query, like_query])

    sql += " ORDER BY DATE(r.return_date) DESC, r.return_id DESC"

    with get_connection() as connection:
        return connection.execute(sql, params).fetchall()
