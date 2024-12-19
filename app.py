import imaplib
import email
from email.header import decode_header

from config import Creds

IMAP_SERVER = "imap.mail.me.com"
IMAP_PORT = 993

def fetch_emails(username, app_specific_password):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        print("Connecting to iCloud IMAP server...")

        mail.login(username, app_specific_password)
        print("Login successful!")

        status, messages = mail.select("INBOX")
        print(status)
        if status != "OK":
            print("Error selecting INBOX!")
            return

        status, message_ids = mail.search(None, 'From "noreply@email.apple.com"')
        if status != "OK":
            print("No emails found.")
            return

        email_ids = message_ids[0].split()  
        print(f"Total emails: {len(email_ids)}")

        # Fetching the latest 10 emails
        latest_email_ids = email_ids[-10:]
        print(latest_email_ids)
        for i in latest_email_ids:
            # res, msg_data = mail.fetch(i, "(RFC822)")  
            res, msg_data = mail.fetch(i, "(BODY.PEEK[])")

            # RFC822(message format)-Retreives the full raw message 
            if res != "OK":
                print(f"Failed to fetch email ID: {i.decode()}")
                continue
           
            with open("email_format.eml", "wb") as file:
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        file.write(response_part[1])


            for response_part in msg_data:
                # print(response_part)
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    froms, encoding = decode_header(msg["From"])[0]
                    if isinstance(froms, bytes):    
                        froms = froms.decode(encoding if encoding else "utf-8")

                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    print(f"Email From: {froms}")
                    print(f"Email Subject: {subject}")
           
        mail.close()
        mail.logout()
        print("Logged out successfully.")

    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    icloud_email = Creds.USERNAME 
    app_password = Creds.APP_PASSWORD

    fetch_emails(icloud_email, app_password)