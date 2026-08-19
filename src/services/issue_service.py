from datetime import date, datetime
from database.connection import get_connection


def issue_book(book_id: int, member_id: int, due_date: str) -> int:
    if not due_date.strip():
        raise ValueError("Due date is required.")

    try:
        datetime.strptime(due_date.strip(), "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Due date must use YYYY-MM-DD format.") from exc

    with get_connection() as connection:
        book = connection.execute(
            """
            SELECT book_id, title, available_quantity
            FROM books
            WHERE book_id = ?
            """,
            (book_id,),
        ).fetchone()

        if book is None:
            raise ValueError("Book not found.")

        member = connection.execute(
            """
            SELECT member_id, name
            FROM members
            WHERE member_id = ?
            """,
            (member_id,),
        ).fetchone()

        if member is None:
            raise ValueError("Member not found.")

        if book["available_quantity"] <= 0:
            raise ValueError("Book is not available.")

        duplicate = connection.execute(
            """
            SELECT issue_id
            FROM issues
            WHERE book_id = ? AND member_id = ? AND returned = 0
            """,
            (book_id, member_id),
        ).fetchone()

        if duplicate is not None:
            raise ValueError("This member already has this book issued.")

        cursor = connection.execute(
            """
            INSERT INTO issues (book_id, member_id, issue_date, due_date, returned)
            VALUES (?, ?, ?, ?, 0)
            """,
            (
                book_id,
                member_id,
                date.today().isoformat(),
                due_date.strip(),
            ),
        )

        connection.execute(
            """
            UPDATE books
            SET available_quantity = available_quantity - 1
            WHERE book_id = ?
            """,
            (book_id,),
        )

        connection.commit()
        return int(cursor.lastrowid)


def list_active_issues():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT
                i.issue_id,
                i.book_id,
                b.title,
                i.member_id,
                m.name AS member_name,
                i.issue_date,
                i.due_date,
                CASE
                    WHEN DATE(i.due_date) < DATE('now') THEN 'Overdue'
                    ELSE 'Active'
                END AS status
            FROM issues i
            JOIN books b ON b.book_id = i.book_id
            JOIN members m ON m.member_id = i.member_id
            WHERE i.returned = 0
            ORDER BY DATE(i.due_date), i.issue_id DESC
            """
        ).fetchall()


def search_active_issues(query: str = ""):
    query = query.strip()

    sql = """
        SELECT
            i.issue_id,
            i.book_id,
            b.title,
            i.member_id,
            m.name AS member_name,
            i.issue_date,
            i.due_date,
            CASE
                WHEN DATE(i.due_date) < DATE('now') THEN 'Overdue'
                ELSE 'Active'
            END AS status
        FROM issues i
        JOIN books b ON b.book_id = i.book_id
        JOIN members m ON m.member_id = i.member_id
        WHERE i.returned = 0
    """
    params = []

    if query:
        like_query = f"%{query}%"
        sql += """
            AND (
                b.title LIKE ?
                OR m.name LIKE ?
                OR CAST(i.issue_id AS TEXT) LIKE ?
                OR CAST(i.book_id AS TEXT) LIKE ?
                OR CAST(i.member_id AS TEXT) LIKE ?
            )
        """
        params.extend(
            [like_query, like_query, like_query, like_query, like_query]
        )

    sql += " ORDER BY DATE(i.due_date), i.issue_id DESC"

    with get_connection() as connection:
        return connection.execute(sql, params).fetchall()


def get_available_books():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT book_id, title, author, available_quantity
            FROM books
            WHERE available_quantity > 0
            ORDER BY title
            """
        ).fetchall()


def get_members():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT member_id, name, course
            FROM members
            ORDER BY name
            """
        ).fetchall()


def get_issue(issue_id: int):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT
                i.issue_id,
                i.book_id,
                b.title,
                i.member_id,
                m.name AS member_name,
                i.issue_date,
                i.due_date,
                i.returned
            FROM issues i
            JOIN books b ON b.book_id = i.book_id
            JOIN members m ON m.member_id = i.member_id
            WHERE i.issue_id = ?
            """,
            (issue_id,),
        ).fetchone()
