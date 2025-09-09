import sqlite3

DB_PATH = "../db/magazines.db"

def create_tables(conn):
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS publishers (
                publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                magazine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                UNIQUE(name, address)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id),
                UNIQUE(subscriber_id, magazine_id)
            )
        """)
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def add_publisher(conn, name):
    try:
        conn.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
    except sqlite3.IntegrityError:
        print(f"Publisher '{name}' already exists.")

def add_magazine(conn, name, publisher_id):
    try:
        conn.execute(
            "INSERT INTO magazines (name, publisher_id) VALUES (?, ?)",
            (name, publisher_id)
        )
    except sqlite3.IntegrityError:
        print(f"Magazine '{name}' already exists or invalid publisher.")

def add_subscriber(conn, name, address):
    try:
        conn.execute(
            "INSERT INTO subscribers (name, address) VALUES (?, ?)",
            (name, address)
        )
    except sqlite3.IntegrityError:
        print(f"Subscriber '{name}, {address}' already exists.")

def add_subscription(conn, subscriber_id, magazine_id, expiration_date):
    try:
        conn.execute(
            "INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)",
            (subscriber_id, magazine_id, expiration_date)
        )
    except sqlite3.IntegrityError:
        print(f"Subscription already exists or invalid IDs.")

def run_queries(conn):
    try:
        print("\nAll subscribers:")
        for row in conn.execute("SELECT * FROM subscribers"):
            print(row)

        print("\nMagazines sorted by name:")
        for row in conn.execute("SELECT * FROM magazines ORDER BY name"):
            print(row)

        print("\nMagazines by a specific publisher (Publisher A):")
        query = """
            SELECT m.magazine_id, m.name
            FROM magazines m
            JOIN publishers p ON m.publisher_id = p.publisher_id
            WHERE p.name = ?
        """
        for row in conn.execute(query, ("Publisher A",)):
            print(row)

    except sqlite3.Error as e:
        print(f"Query error: {e}")

def main():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = 1")

        create_tables(conn)

        # Populate data
        add_publisher(conn, "Publisher A")
        add_publisher(conn, "Publisher B")
        add_publisher(conn, "Publisher C")

        add_magazine(conn, "Tech Monthly", 1)
        add_magazine(conn, "Health Weekly", 2)
        add_magazine(conn, "Travel Guide", 3)

        add_subscriber(conn, "Alice", "123 Main St")
        add_subscriber(conn, "Bob", "456 Oak Ave")
        add_subscriber(conn, "Charlie", "789 Pine Rd")

        add_subscription(conn, 1, 1, "2026-01-01")
        add_subscription(conn, 2, 2, "2026-02-15")
        add_subscription(conn, 3, 3, "2026-03-10")

        conn.commit()

        run_queries(conn)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
