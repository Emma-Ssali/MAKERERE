import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.core.mail import EmailMessage
from django.conf import settings
import os


def send_email_with_attachment(recipient_email, subject, body, attachment_path):
    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Add body to email
        msg.attach(MIMEText(body, 'plain'))

        # Open the file to be sent
        attachment = open(attachment_path, 'rb')

        # Add file as application/octet-stream
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)

        # Add header
        part.add_header('Content-Disposition', f'attachment; filename= {attachment_path}')

        # Attach file to message
        msg.attach(part)

        # Send email using Django's EmailMessage class
        email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [recipient_email])
        email.attach_file(attachment_path)
        email.send()

        print(f"Email with attachment sent successfully to {recipient_email}")
        return True

    except Exception as e:
        print(f"Error sending email with attachment to {recipient_email}: {str(e)}")
        return False