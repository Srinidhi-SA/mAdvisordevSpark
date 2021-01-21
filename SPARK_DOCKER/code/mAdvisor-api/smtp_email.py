from __future__ import print_function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from django.conf import settings

username = 'ankush.patel@marlabs.com'  # Email Address from the email you want to send an email
password = 'Marlabs@123'  # Password)

"""
SMTP Server Information
1. Gmail.com: smtp.gmail.com:587
2. Outlook.com: smtp-mail.outlook.com:587
3. Office 365: outlook.office365.com
Please verify your SMTP settings info.
"""

# Create the body of the message (a HTML version for formatting).
html = """There is some error."""

from_addr = username


def send_mail(username, password, from_addr, to_addrs, msg):
    """send email."""
    server = smtplib.SMTP('smtp-mail.outlook.com', '587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()


def send_alert_through_email(error=None):
    jobserver_sender_email = 'ankush.patel@marlabs.com'
    jobserver_email_template = "Problem IP-"

    # for to_addrs in joserver_email_list:
    msg = MIMEMultipart()

    msg['Subject'] = "MARLABS-ERROR"
    msg['From'] = jobserver_sender_email
    msg['To'] = " ,".join(settings.LIST_OF_ADMIN_EMAILS)

    html = jobserver_email_template + "  {0}".format(error)
    # Attach HTML to the email
    body = MIMEText(html, 'html')
    msg.attach(body)

    # Attach Cover Letter to the email
    # cover_letter = MIMEApplication(open("file1.pdf", "rb").read())
    # cover_letter.add_header('Content-Disposition', 'attachment', filename="file1.pdf")
    # msg.attach(cover_letter)

    # Attach Resume to the email
    # cover_letter = MIMEApplication(open("file2.pdf", "rb").read())
    # cover_letter.add_header('Content-Disposition', 'attachment', filename="file2.pdf")
    # msg.attach(cover_letter)

    try:
        print("Senging emails to", " ,".join(settings.LIST_OF_ADMIN_EMAILS))
        send_mail(username, password, from_addr, settings.LIST_OF_ADMIN_EMAILS, msg)
        print("Email successfully sent to", " ,".join(settings.LIST_OF_ADMIN_EMAILS))
    except smtplib.SMTPAuthenticationError:
        print('SMTPAuthenticationError')
        print("Email not sent to", settings.LIST_OF_ADMIN_EMAILS)
