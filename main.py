import logging
import ssl
from smtplib import SMTP, SMTPAuthenticationError
from config import DISPLAY_NAME, EMAIL_ADDRESS, EMAIL_PASSWORD, HOST, PORT
import utils

if __name__ == "__main__":
    environment_status, environment_code = utils.check_and_create_directories()
    print(environment_code)

    if environment_status:
    
        context = ssl.create_default_context()

        with SMTP(host=HOST, port=PORT) as server:
            
            server.starttls(context=context)
            try:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                print("✅  Successful login to the email\n")
                print("---------ACCOUNT---------")
                print(f"Display Name: {DISPLAY_NAME}")
                print(f"Sender Email: {EMAIL_ADDRESS}\n")
                logging.info("Started email sending process")
                utils.send_emails(server, DISPLAY_NAME, EMAIL_ADDRESS, EMAIL_PASSWORD)
                logging.info("Finished email sending process")
            except SMTPAuthenticationError as e:
                logging.error("Failed to authenticate with the email server: %s", str(e))
                print("ERROR: Failed to authenticate with the email server.")
            except Exception as e:
                logging.error("An unexpected error occurred: %s", str(e))
                print("An unexpected error occurred.")
    else:
        exit()
