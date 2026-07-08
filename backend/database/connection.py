import sqlite3

from config import DATABASE_PATH

# Create SQLite connection
connection = sqlite3.connect(
    DATABASE_PATH,
    check_same_thread=False
)
# Return rows as dictionary-like objects
connection.row_factory = sqlite3.Row

# Create cursor
cursor = connection.cursor()
def get_cursor():
    return connection.cursor()