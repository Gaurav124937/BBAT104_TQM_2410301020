from utils.validation import non_negative_integer, require_text
from typing import Optional
from database.connection import get_connection


def add_book(
    title: str,
    author: str,
    category: str,
    isbn: Optional[str],
    quantity: int,
) -> int:
    title = require_text(title, "Title")
    author = require_text(author, "Author")
    category = require_text(category, "Category")
    isbn = isbn.strip() if isbn else None
    quantity = non_negative_integer(quantity, "Quantity")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO books
            (title, author, category, isbn, quantity, available_quantity)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, author, category, isbn, quantity, quantity),
        )
        connection.commit()
        return int(cursor.lastrowid)


def list_books():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT book_id, title, author, category, isbn,
                   quantity, available_quantity
            FROM books
            ORDER BY book_id DESC
            """
        ).fetchall()


def search_books(query: str = "", category: str = "", availability: str = "All"):
    query = query.strip()
    category = category.strip()

    sql = """
        SELECT book_id, title, author, category, isbn,
               quantity, available_quantity
        FROM books
        WHERE 1 = 1
    """
    params = []

    if query:
        sql += """
            AND (
                title LIKE ?
                OR author LIKE ?
                OR isbn LIKE ?
            )
        """
        like_query = f"%{query}%"
        params.extend([like_query, like_query, like_query])

    if category and category != "All":
        sql += " AND category = ?"
        params.append(category)

    if availability == "Available":
        sql += " AND available_quantity > 0"
    elif availability == "Unavailable":
        sql += " AND available_quantity = 0"

    sql += " ORDER BY book_id DESC"

    with get_connection() as connection:
        return connection.execute(sql, params).fetchall()


def get_book(book_id: int):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT book_id, title, author, category, isbn,
                   quantity, available_quantity
            FROM books
            WHERE book_id = ?
            """,
            (book_id,),
        ).fetchone()


def update_book(
    book_id: int,
    title: str,
    author: str,
    category: str,
    isbn: Optional[str],
    quantity: int,
) -> None:
    title = require_text(title, "Title")
    author = require_text(author, "Author")
    category = require_text(category, "Category")
    isbn = isbn.strip() if isbn else None
    quantity = non_negative_integer(quantity, "Quantity")

    with get_connection() as connection:
        current = connection.execute(
            """
            SELECT quantity, available_quantity
            FROM books
            WHERE book_id = ?
            """,
            (book_id,),
        ).fetchone()

        if current is None:
            raise ValueError("Book not found.")

        issued_count = current["quantity"] - current["available_quantity"]

        if quantity < issued_count:
            raise ValueError(
                f"Quantity cannot be less than currently issued copies ({issued_count})."
            )

        new_available = quantity - issued_count

        connection.execute(
            """
            UPDATE books
            SET title = ?,
                author = ?,
                category = ?,
                isbn = ?,
                quantity = ?,
                available_quantity = ?
            WHERE book_id = ?
            """,
            (
                title,
                author,
                category,
                isbn,
                quantity,
                new_available,
                book_id,
            ),
        )
        connection.commit()


def delete_book(book_id: int) -> None:
    with get_connection() as connection:
        active_issues = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM issues
            WHERE book_id = ? AND returned = 0
            """,
            (book_id,),
        ).fetchone()["count"]

        if active_issues:
            raise ValueError("Cannot delete a book that is currently issued.")

        result = connection.execute(
            "DELETE FROM books WHERE book_id = ?",
            (book_id,),
        )

        if result.rowcount == 0:
            raise ValueError("Book not found.")

        connection.commit()


def get_categories():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT DISTINCT category
            FROM books
            WHERE category IS NOT NULL AND TRIM(category) <> ''
            ORDER BY category
            """
        ).fetchall()
        return [row["category"] for row in rows]
