# services/auth.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()


def send_email(to_email: str, subject: str, content: str):
    sender_email = os.getenv("GMAIL_ADDRESS")
    smtp_password = os.getenv("GMAIL_APP_PASSWORD")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 500px; margin: auto; background: white; border-radius: 8px; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                <h2 style="color: #333;">🔐 Your One-Time Password (OTP)</h2>
                <p style="font-size: 16px; color: #555;">
                    Please use the following code to complete your <strong>{subject.lower()}</strong> process:
                </p>
                <div style="font-size: 24px; font-weight: bold; color: #111; margin: 20px 0; text-align: center;">
                    {content}
                </div>
                <p style="font-size: 14px; color: #999;">
                    This code will expire in 10 minutes. If you didn’t request this, please ignore this email.
                </p>
                <p style="font-size: 14px; color: #ccc; text-align: center; margin-top: 40px;">
                    Spotnxt Team • Empowering Smart Advertising
                </p>
            </div>
        </body>
    </html>
    """

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
