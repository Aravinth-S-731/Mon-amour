import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime
import threading

load_dotenv()

sender_email = os.getenv("EMAIL_USER")
sender_password = os.getenv("EMAIL_PASS")

def send_notification_email(subject, body, to_email=sender_email):
    """Send email in background thread to avoid blocking requests."""
    def send():
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_body = f"{body}\n\nTimestamp: {timestamp}"
        msg.attach(MIMEText(full_body, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
                print("✅ Email sent successfully.")
        except Exception as e:
            print("❌ Failed to send email:", str(e))
    
    # Send email in background (non-blocking)
    thread = threading.Thread(target=send, daemon=True)
    thread.start()
