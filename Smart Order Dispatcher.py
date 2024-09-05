import imaplib
import email
from email.header import decode_header
import spacy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables (email credentials and server settings)
load_dotenv()
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
IMAP_SERVER = os.getenv('IMAP_SERVER')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Function to connect and fetch emails
def fetch_emails():
    # Connect to the email server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    
    # Search for all emails
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()

    # Process the latest email
    for email_id in email_ids[-1:]:  # Change slice to adjust how many emails to process
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                from_ = msg.get("From")
                print("Subject:", subject)
                print("From:", from_)

                # Extract email body
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            continue
                        if content_type == "text/plain":
                            process_order(body)
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                    process_order(body)

    # Close the connection
    mail.logout()

# Function to process the order using NLP
def process_order(email_body):
    # Extract order details using spaCy
    doc = nlp(email_body)
    order_details = {
        "products": [],
        "quantities": [],
        "dates": []
    }

    for ent in doc.ents:
        if ent.label_ in ["PRODUCT", "ORG"]:  # Customize based on your needs
            order_details["products"].append(ent.text)
        elif ent.label_ == "CARDINAL":  # Assuming quantities are identified as CARDINAL
            order_details["quantities"].append(ent.text)
        elif ent.label_ == "DATE":
            order_details["dates"].append(ent.text)
    
    print("Extracted Order Details:", order_details)

    # Dummy logic to determine recipient based on extracted data
    recipient_email = determine_recipient(order_details)
    if recipient_email:
        send_email(recipient_email, order_details)

# Function to determine which employee should receive the order
def determine_recipient(order_details):
    # Simple logic to choose recipient based on product names
    # Replace this with actual logic for your application
    if "Product A" in order_details["products"]:
        return "employeeA@example.com"
    elif "Product B" in order_details["products"]:
        return "employeeB@example.com"
    else:
        return "default@example.com"

# Function to send an email to the determined recipient
def send_email(recipient_email, order_details):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = recipient_email
    msg['Subject'] = "New Order Received"

    body = f"Order Details:\nProducts: {', '.join(order_details['products'])}\nQuantities: {', '.join(order_details['quantities'])}\nDates: {', '.join(order_details['dates'])}"
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        print(f"Email sent to {recipient_email}")

if __name__ == "__main__":
    fetch_emails()
