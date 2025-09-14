import sqlite3

def print_db_contents(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Filter tables to keep only 'table', 'books', and 'users'
    tables = [t for t in tables if t[0] in ('table', 'books', 'users')]
    for table_name in tables:
        print(f"Table: {table_name[0]}")
        cursor.execute(f"SELECT * FROM {table_name[0]}")
        rows = cursor.fetchall()
        # Get column names
        col_names = [description[0] for description in cursor.description]
        print(" | ".join(col_names))
        for row in rows:
            print(" | ".join(str(item) for item in row))
        print("-" * 40)

    conn.close()

if __name__ == "__main__":
    print_db_contents("library.db")