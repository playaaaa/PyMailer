# PyMailer
Automated Email-sending script


This project is an automated email-sending script written in Python. It allows you to send customized emails to a list of recipients stored in a CSV file, using a markdown-based email template. The script handles logging, manages email attachments, saves sent emails to a specified folder, and respects email-sending delay intervals to prevent spam detection.

## Features

- **Send Emails:** Automatically send emails using a markdown-based template.
- **Save Sent Emails:** Store sent emails in a specified folder on the IMAP server.
- **CSV-Based Recipients:** Read recipient information from a CSV file and personalize each email.
- **Attach Files:** Optionally attach a file to each email.
- **Email Delay:** Configure a delay between each sent email to avoid sending too many emails in a short period.
- **Folder and File Check:** Automatically create required folders and check if necessary files exist before starting the email-sending process.

## Project Structure

- `main.py`: The entry point of the script, handles SMTP connection and starts the email-sending process.
- `utils.py`: Contains helper functions for managing directories, reading templates, attaching files, and sending emails.
- `config.py`: Stores configuration variables such as SMTP server details, email credentials, file paths, and other settings.

## Prerequisites

Before running the script, ensure you have the following:

- **Python 3.7+**
- **Required Python Packages**:
  - `markdown`

You can install the required packages using:

```bash
pip install -r requirements.txt
```

## Configuration

Modify the `config.py` file to suit your email server settings:

- `HOST`: SMTP server address (e.g., `smtp.mail.ru` or `smtp.gmail.com`)
- `HOST_IMAP`: IMAP server address for saving sent emails.
- `PORT`: Port number for the SMTP server (typically `587`).
- `DISPLAY_NAME`: The name that will be displayed as the sender.
- `EMAIL_ADDRESS`: Your email address.
- `EMAIL_PASSWORD`: An application-specific password for sending emails.
- `EMAIL_TEXT`: The markdown file containing the email template.
- `DATABASE`: The CSV file with recipient data.
- `FOLDER_TO_SAVE`: IMAP folder name where sent emails will be saved.
- `ADDITIONAL_FILE`: Optional file to attach to each email.
- `EMAIL_DELAY_MIN` and `EMAIL_DELAY_MAX`: Minimum and maximum delay between sending each email.

P.S
- `HOST` (smtp.mail.ru - i recommend it for Russia | smtp.gmail.com - for Gmail | if it doesn't work, change it to something else)
- `PORT` (you can check port for your host in google :)
- `EMAIL_PASSWORD` (Email password | NOT from your Email !!! set up an App Password for automailer)
- `FOLDER_TO_SAVE` ("&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-" for Mail.ru (IMAP_UTF-7 decode) | 'Sent' for Gmail | for others you can look at the utils.py the commented-out function list_folders)

## Email Template

The email template should be a markdown file (e.g., `example.md`) with the following structure:

```
Subject of the Email
---
Hello, $NAME

This is a personalized message for you.
```

- The first line will be used as the subject.
- `$NAME` will be replaced by the corresponding value from the CSV file for each recipient.

## CSV File Structure

The CSV file (e.g., `example.csv`) should have the following structure:

```csv
EMAIL,NAME
recipient1@example.com,John Doe
recipient2@example.com,Jane Smith
```

- `EMAIL`: Recipient's email address.
- `NAME`: Recipient's name (or other variables that you want to use in the template).

## How to Run

1. **Ensure all required files and directories are in place**:
   - Create the following directories if they do not exist:
     - `additional_files`
     - `databases`
     - `texts`
   - Place your email template in the `texts` folder and your recipient CSV in the `databases` folder.

2. **Start the Script**:

   ```bash
   python main.py
   ```

3. **Confirm Sending**:
   - You will be prompted to confirm the email-sending process. Enter `y` to proceed or `n` to cancel.

## Logging

Logs are stored in `logs/email_sending.log` and provide detailed information about the email-sending process, including successful email deliveries and any errors encountered.

## Error Handling

- **SMTPAuthenticationError**: If login fails, ensure that the `EMAIL_PASSWORD` is set correctly and that you have enabled access for less secure apps or used an app password.
- **Missing Files**: The script will create required folders but will log an error if the necessary template or database files are missing.
- **Attachment Issues**: If an attachment is specified but not found, a warning will be logged and the email will be sent without the attachment.
