from utils.validation import require_text
from typing import Optional
from database.connection import get_connection


def add_member(
    name: str,
    course: str,
    phone: str = "",
    email: str = "",
) -> int:
    name = require_text(name, "Name")
    course = require_text(course, "Course")
    phone = phone.strip()
    email = email.strip()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO members (name, course, phone, email)
            VALUES (?, ?, ?, ?)
            """,
            (name, course, phone, email),
        )
        connection.commit()
        return int(cursor.lastrowid)


def list_members():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT member_id, name, course, phone, email
            FROM members
            ORDER BY member_id DESC
            """
        ).fetchall()


def search_members(query: str = "", course: str = ""):
    query = query.strip()
    course = course.strip()

    sql = """
        SELECT member_id, name, course, phone, email
        FROM members
        WHERE 1 = 1
    """
    params = []

    if query:
        sql += """
            AND (
                name LIKE ?
                OR phone LIKE ?
                OR email LIKE ?
                OR CAST(member_id AS TEXT) LIKE ?
            )
        """
        like_query = f"%{query}%"
        params.extend([like_query, like_query, like_query, like_query])

    if course and course != "All":
        sql += " AND course = ?"
        params.append(course)

    sql += " ORDER BY member_id DESC"

    with get_connection() as connection:
        return connection.execute(sql, params).fetchall()


def get_member(member_id: int):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT member_id, name, course, phone, email
            FROM members
            WHERE member_id = ?
            """,
            (member_id,),
        ).fetchone()


def update_member(
    member_id: int,
    name: str,
    course: str,
    phone: str = "",
    email: str = "",
) -> None:
    name = require_text(name, "Name")
    course = require_text(course, "Course")
    phone = phone.strip()
    email = email.strip()

    with get_connection() as connection:
        result = connection.execute(
            """
            UPDATE members
            SET name = ?, course = ?, phone = ?, email = ?
            WHERE member_id = ?
            """,
            (name, course, phone, email, member_id),
        )

        if result.rowcount == 0:
            raise ValueError("Member not found.")

        connection.commit()


def delete_member(member_id: int) -> None:
    with get_connection() as connection:
        active_issues = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM issues
            WHERE member_id = ? AND returned = 0
            """,
            (member_id,),
        ).fetchone()["count"]

        if active_issues:
            raise ValueError("Cannot delete a member with an active issued book.")

        result = connection.execute(
            "DELETE FROM members WHERE member_id = ?",
            (member_id,),
        )

        if result.rowcount == 0:
            raise ValueError("Member not found.")

        connection.commit()


def get_courses():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT DISTINCT course
            FROM members
            WHERE course IS NOT NULL AND TRIM(course) <> ''
            ORDER BY course
            """
        ).fetchall()
        return [row["course"] for row in rows]
