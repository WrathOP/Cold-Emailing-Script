from email.mime.base import MIMEBase
import os
import io
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
import sqlite3

# importing insert_emails_to_db function from insert-emails-to-db.py
from insertEmailsToDB import insert_emails_to_db


def send_email(
    sender_email,
    receiver_email,
    subject,
    message,
    smtp_server,
    smtp_port,
    sender_password,
    part,
):
    # Create a MIMEText object to represent the email
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email
    email["Subject"] = subject

    # Attach the attachment to the email
    email.attach(part)

    # Attach the message to the email
    email.attach(MIMEText(message, "plain"))

    # Connect to the SMTP server
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            print("Logging in")
            server.login(sender_email, sender_password)  # Login to the SMTP server
            print("Logged in, Sending email")
            server.send_message(email)  # Send the email
    except Exception as e:
        print(f"An error occurred while sending email: {e}")


def main():
    # Load environment variables
    load_dotenv()
    conn = sqlite3.connect("emails.db")    
    cursor = conn.cursor()

    # Get the environment variables
    sender_email = os.environ["SENDER_EMAIL"]
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_port = os.environ["SMTP_PORT"]  # Port for TLS
    sender_password = os.environ["SENDER_PASSWORD"]
    name = os.environ["YOUR_NAME"]

    # Pipe my resume as an octet-stream for the attachment (Could have used application/pdf as well)
    with open("./resume.pdf", "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename={name}_resume.pdf",  # Specify the filename here
    )

    # pipe recievers email from emails.txt to this variable and for loop to send email to recievers
    file = io.open("emails.txt", "r")

    for line in file.readlines():

        # Searching if the file is already sent to the email
        email = cursor.execute("SELECT recipient FROM sent_emails WHERE recipient=?", (line.strip(),)).fetchone()

        if email is None:
            receiver_email = line
            print("Sending Email to :", receiver_email)
            send_email(
                sender_email,
                receiver_email,
                subject,
                message,
                smtp_server,
                smtp_port,
                sender_password,
                part,
            )
            try:
                cursor.execute("INSERT INTO sent_emails (recipient, subject, message) VALUES (?, ?, ?)", (receiver_email.strip(), subject, message))
                conn.commit()  # Commit the transaction to persist changes
                print(f"Email sent to {receiver_email} and added to the database")
            except sqlite3.Error as e:
                print("Error occurred during insertion:", e)
        else: 
            print("Email already sent to ", line)

    # close the connection to the database
    conn.close()
    # close the file
    file.close()


# Example usage
if __name__ == "__main__":

    subject = "Passionate SDE Seeking Opportunity to Contribute"
    message = """ 
    Hi there,

    I hope this email finds you well. I'm currently interning at Debound in Delhi as a Flutter Engineer cum Full Stack Developer, following a stint at Mrikal Studio as a Full Stack Intern.

    I'm reaching out to express my interest in the Software Development Engineer position at your company. I am confident that my skills and experience make me an excellent candidate for the job.

    My skills include: Flutter, React, Node.js, Express.js, MongoDB, Firebase, Git, HTML, CSS, JavaScript, Python, C++, Java, SQL, RESTful APIs, and more.

    Not only do I have the technical skills required for the job, but I also have a passion for software development. I am always looking for ways to improve my skills and learn new technologies. I am confident that I can make a positive contribution to your team. I would love the opportunity to discuss how my skills and experiences can benefit your company.

    I have attached my resume for your review. Please let me know if you have any questions or if you would like to schedule an interview. I look forward to hearing from you.

    Thank you for your time and consideration.

    Pratham Mittal
    """
    main()

# For bulk email setting in the database
# insert_emails_to_db(message, './emails.txt', db_file_path='emails.db', table_name='sent_emails',subject=subject)
