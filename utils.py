import csv
import os
import logging
import markdown
import random
import time
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.header import Header
from config import HOST, PORT, DISPLAY_NAME, EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_TEXT, DATABASE, ADDITIONAL_FILE, EMAIL_DELAY_MIN, EMAIL_DELAY_MAX, HOST_IMAP, FOLDER_TO_SAVE


def check_and_create_directories():
    directories = ["logs", "additional_files", "databases", "texts"]
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Creating folder: {directory}")
            os.makedirs(directory)
            
        
    logging.basicConfig(
    filename='logs/email_sending.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

    files_to_check = {
        f"./databases/{DATABASE}": "Database file",
        f"./texts/{EMAIL_TEXT}": "Mail text (md) file"
    }

    if ADDITIONAL_FILE:
        additional_file_path = f"./additional_files/{ADDITIONAL_FILE}"
        files_to_check[additional_file_path] = "Additional file"
    else:
        print("⚠️  WARNING: Additional File is not specified!")

    for file_path, description in files_to_check.items():
        if not os.path.isfile(file_path):
            logging.error(f"{description} {file_path} not found.")
            return False, f"ERROR: {description} {file_path} not found."

    required_config = {
        "HOST": HOST,
        "PORT": PORT,
        "DISPLAY_NAME": DISPLAY_NAME,
        "EMAIL_ADDRESS": EMAIL_ADDRESS,
        "EMAIL_PASSWORD": EMAIL_PASSWORD
    }

    for key, value in required_config.items():
        if not value:
            logging.error(f"The configuration variable {key} is not set.")
            return False, f"ERROR: The configuration variable {key} is not set."
        
    return True, "✅ Success: All files are uploaded!"

def get_msg(csv_file_path, template):
    try:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            headers = file.readline().strip().split(",")
    except Exception as e:
        logging.error(f"Error reading CSV headers: {e}")
        return

    try:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            data = csv.DictReader(file)
            for row in data:
                required_string = template
                for header in headers:
                    value = row.get(header, "")
                    required_string = required_string.replace(f"${header}", value)
                yield row["EMAIL"], required_string
    except Exception as e:
        logging.error(f"Error reading CSV data: {e}")

def attach_file(multipart_msg, file_path, file_name):
    if not os.path.isfile(file_path):
        logging.warning(f"Additional file {file_path} not found, skipping it...")
        return

    try:
        with open(file_path, "rb") as f:
            attach_part = MIMEBase("application", "octet-stream")
            attach_part.set_payload(f.read())
            encoders.encode_base64(attach_part)
            attach_part.add_header("Content-Disposition", f"attachment; filename*=UTF-8''{file_name}")
            multipart_msg.attach(attach_part)
    except Exception as e:
        logging.error(f"Error attaching file {file_name}: {e}")


def save_to_sent(email_address, email_password, message):
    try:
        imap_server = imaplib.IMAP4_SSL(HOST_IMAP)
        imap_server.login(email_address, email_password)
        imap_server.append(f'"{FOLDER_TO_SAVE}"', '', imaplib.Time2Internaldate(time.time()), message.encode('utf-8'))

        print(f"✅ The message has been saved to a folder '{FOLDER_TO_SAVE}'.")
        logging.info(f"The message has been saved to a folder '{FOLDER_TO_SAVE}'.")
        
        imap_server.logout()
    except Exception as e:
        logging.error(f"ERROR: The message could not be saved to a folder '{FOLDER_TO_SAVE}': {e}")
        print(f"ERROR: when saving an email to '{FOLDER_TO_SAVE}': {e}")


def send_emails(server, display_name, email_address, email_password):
    try:
        with open(f"texts/{EMAIL_TEXT}", "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        logging.error(f"Template file {EMAIL_TEXT} not found.")
        return
    except Exception as e:
        logging.error(f"Error reading template file: {e}")
        return

    confirmation = input("Are you sure you want to start sending emails? (y/n): ").lower()

    if confirmation != "y":
        print("The sending of emails has been canceled.")
        logging.info("The sending of emails has been canceled")
        return

    print("Starting to send emails...")
    logging.info("Starting to send emails...")

    sent_count = 0

    template_lines = template.strip().split("\n", 1)
    email_subject = template_lines[0].strip()
    email_body = template_lines[1].strip() if len(template_lines) > 1 else ""

    try:
        for receiver, message in get_msg(f"./databases/{DATABASE}", email_body):
            multipart_msg = MIMEMultipart("alternative")
            multipart_msg["Subject"] = str(Header(email_subject, 'utf-8'))
            multipart_msg["From"] = f"{str(Header(display_name, 'utf-8'))} <{email_address}>"
            multipart_msg["To"] = receiver

            text = message
            html = markdown.markdown(text)

            part1 = MIMEText(text, "plain", "utf-8")
            part2 = MIMEText(html, "html", "utf-8")

            multipart_msg.attach(part1)
            multipart_msg.attach(part2)

            if ADDITIONAL_FILE:
                attach_file(multipart_msg, f"./additional_files/{ADDITIONAL_FILE}", ADDITIONAL_FILE)

            try:
                server.sendmail(email_address, receiver, multipart_msg.as_string())
                logging.info(f"Email sent to {receiver}")
                print(f"Email sent to {receiver}")
                sent_count += 1
                
                #list_folders(email_address, email_password)
                save_to_sent(email_address, email_password, multipart_msg.as_string())

                delay = random.uniform(EMAIL_DELAY_MIN, EMAIL_DELAY_MAX)
                logging.info(f"Waiting for {delay:.2f} seconds before sending the next email...")
                print(f"Waiting for {delay:.2f} seconds before sending the next email...")
                time.sleep(delay)

            except Exception as err:
                logging.error(f"Failed to send email to {receiver}: {err}")
                print(f"Problem occurred while sending to {receiver}")
                input("PRESS ENTER TO CONTINUE")
    except Exception as e:
        logging.error(f"Error during email sending process: {e}")

    print(f"Sent {sent_count} emails")
    logging.info(f"Sent {sent_count} emails")




""" FUNCTION TO FIND ALL FOLDERS
def list_folders(email_address, email_password):
    try:
        imap_server = imaplib.IMAP4_SSL(HOST_IMAP)
        imap_server.login(email_address, email_password)

        status, folders = imap_server.list()

        if status == 'OK':
            print("List of available folders:")
            for folder in folders:
                print(folder.decode())
        else:
            print("An error occurred when retrieving the folder list.")
        
        imap_server.logout()
    except Exception as e:
        print(f"Error connecting or retrieving the folder list: {e}")
"""