from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_DIR = ROOT_DIR / "database"
DB_PATH = DB_DIR / "library.db"
DB_DIR.mkdir(parents=True, exist_ok=True)

def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
