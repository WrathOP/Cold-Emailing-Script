from email.mime.base import MIMEBase
import os
import io
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders


def send_email(
    sender_email,
    receiver_email,
    subject,
    message,
    smtp_server,
    smtp_port,
    sender_password,
    part
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
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)  # Login to the SMTP server
        server.send_message(email)  # Send the email

    print("Email sent successfully! to ", receiver_email)


# Example usage
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    # Get the environment variables
    sender_email = os.environ["SENDER_EMAIL"]
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_port = os.environ["SMTP_PORT"]  # Port for TLS
    sender_password = os.environ["SENDER_PASSWORD"]

    subject = "Sending in resume for the Software developer position at your company."
    message = "This is a test email sent from Python."

    # Pipe my resume as an octet-stream for the attachment (Could have used application/pdf as well)
    with open("./Pratham_Mittal_Resume.pdf", "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename=Pratham_Mittal_Resume.pdf",  # Specify the filename here
    )

    # pipe recievers email from emails.txt to this variable and for loop to send email to recievers
    file = io.open("emails.txt", "r")

    for line in file.readlines():
        print("Sending Email to :", line)
        receiver_email = line
        send_email(
            sender_email,
            receiver_email,
            subject,
            message,
            smtp_server,
            smtp_port,
            sender_password,
            part
        )