import sqlite3

def insert_emails_to_db(message, emails_file_path, db_file_path='emails.db', table_name='sent_emails',subject='Subject of the email'):

    # Connect to the SQLite database
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()

    # Open the text file containing emails
    with open('emails.txt', 'r') as file:
        emails = file.readlines()

        # Insert each email into the database
        for email in emails:
            cursor.execute(f"INSERT INTO {table_name} (recipient, subject, message) VALUES (?, ?, ?)", (email.strip(),subject, message))

    # Commit changes and close connection
    conn.commit()
    conn.close()

