import imaplib
import email
from email.header import decode_header

# Email configuration
email_user = "your_email@example.com"
email_password = "your_password"
imap_server = "imap.example.com"

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(email_user, email_password)

# Select the mailbox you want to work with (e.g., "INBOX")
mailbox = "INBOX"
mail.select(mailbox)

# Search for all emails in the mailbox
status, email_ids = mail.search(None, "ALL")
email_ids = email_ids[0].split()

# Loop through email IDs
for email_id in email_ids:
    # Fetch the email
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])

    # Get the sender's email address
    sender = msg["From"]

    # Categorize and label emails based on sender's domain
    if "example.com" in sender:
        # Move email to a "Example" folder
        mail.copy(email_id, "Example")
        mail.store(email_id, '+FLAGS', '(\Deleted)')
    elif "otherdomain.com" in sender:
        # Move email to an "Other Domain" folder
        mail.copy(email_id, "Other Domain")
        mail.store(email_id, '+FLAGS', '(\Deleted)')

# Expunge deleted emails
mail.expunge()

# Logout and close the connection
mail.logout()
