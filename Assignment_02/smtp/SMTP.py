# B. SMTP
#  • Write a Python program to:
#  1. Connect to an SMTP server.
#  2. Send a test email to a recipient address.
#  3. Log the communication process for reference.

# smtp_client.py - Ethereal SMTP
import smtplib
from email.mime.text import MIMEText

# Ethereal credentials
#Ethereal link: https://ethereal.email/?utm_source=chatgpt.com
sender_email = "marion.collier61@ethereal.email"
receiver_email = "marion.collier61@ethereal.email"
password = "jNQt7XcRGQ8sejCvFm"  # Ethereal account password

try:
    # Create email message
    msg = MIMEText("Hello! This is a test email from Python (Ethereal test).")
    msg["Subject"] = "CN Assignment_02 SMTP Email"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Connect to Ethereal SMTP server
    server = smtplib.SMTP("smtp.ethereal.email", 587)
    #server = smtplib.SMTP("smtp.gmail.com", 587)
    #server.set_debuglevel(1)  # log communication
    server.starttls()  # secure connection
    server.login(sender_email, password)

    # Send email
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print("✅ Email sent successfully! Check Ethereal inbox.")

    server.quit()
except Exception as e:
    print("❌ Error:", e)
