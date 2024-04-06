# Sending Emails with Python

This repository contains a Python script for sending emails using SMTP. Before using the script, please follow the instructions below to set up your environment.

## Setup Instructions

1. Rename the `.envsample` file to `.env`.
2. Fill in the required fields in the `.env` file:
   - `SMTP_SERVER`: The SMTP server address (e.g., smtp.gmail.com).
   - `SMTP_PORT`: The SMTP server port number (e.g., 587 for TLS).
   - `SENDER_EMAIL`: Your email address from which the email will be sent.
   - `SENDER_PASSWORD`: Your app password generated for sending emails (see below for instructions).
3. Follow the instructions below to generate an app password for sending emails.

## Generating an App Password

To send emails using this script, you'll need to generate an app password if you have two-step verification enabled. Follow these steps to generate an app password:

1. [Activate two-step verification](https://www.google.com/landing/2step/) for your Google account if you haven't already done so.
2. Go to your Google Account settings.
3. Navigate to the "Security" section.
4. Under "Signing in to Google," click on "App passwords" or a similar option.
5. Select "Mail" and "Other (Custom name)" from the dropdown menus.
6. Enter a name for your app password (e.g., "Python Email Script").
7. Click on "Generate."
8. Copy the generated app password (a sixteen-digit password).
9. Paste the app password into the `SENDER_PASSWORD` field in your `.env` file.

## Running the Script

After setting up your `.env` file and generating the app password, you can run the Python script to send emails using the configured settings.

```python
# Import necessary libraries and define the send_email function

# Load variables from the .env file
load_dotenv()

# Access the variables using os.environ()
sender_email = os.environ["SENDER_EMAIL"]
smtp_server = os.environ["SMTP_SERVER"]
smtp_port = os.environ["SMTP_PORT"]  # Port for TLS
sender_password = os.environ["SENDER_PASSWORD"]
name = os.environ["YOUR_NAME"]



# Call the send_email function with the retrieved variables
send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, sender_password,part)
