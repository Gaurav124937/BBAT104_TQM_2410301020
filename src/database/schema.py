from database.connection import get_connection

SCHEMA = [
    """CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT NOT NULL,
        isbn TEXT UNIQUE,
        quantity INTEGER NOT NULL CHECK(quantity >= 0),
        available_quantity INTEGER NOT NULL CHECK(available_quantity >= 0 AND available_quantity <= quantity)
    )""",
    """CREATE TABLE IF NOT EXISTS members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        course TEXT NOT NULL,
        phone TEXT,
        email TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS issues (
        issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        issue_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        returned INTEGER NOT NULL DEFAULT 0 CHECK(returned IN (0,1)),
        FOREIGN KEY(book_id) REFERENCES books(book_id),
        FOREIGN KEY(member_id) REFERENCES members(member_id)
    )""",
    """CREATE TABLE IF NOT EXISTS returns (
        return_id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_id INTEGER NOT NULL UNIQUE,
        return_date TEXT NOT NULL,
        FOREIGN KEY(issue_id) REFERENCES issues(issue_id)
    )""",
]

def initialize_database() -> None:
    with get_connection() as connection:
        for statement in SCHEMA:
            connection.execute(statement)
        connection.commit()
