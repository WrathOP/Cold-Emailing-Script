import sqlite3

# Run this script to create the database and tables
def create_database():
    try:
        conn = sqlite3.connect("emails.db")
        cursor = conn.cursor()

        # Drop table if it exists
        cursor.execute("DROP TABLE IF EXISTS sent_emails")

        # Create table for sent emails
        cursor.execute('''
            CREATE TABLE sent_emails (
                id INTEGER PRIMARY KEY,
                recipient TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create index on recipient column
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_recipient ON sent_emails (recipient)
        ''')

        conn.commit()
        print("Database and tables created successfully.")

    except sqlite3.Error as e:
        print("Error occurred:", e)

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()
