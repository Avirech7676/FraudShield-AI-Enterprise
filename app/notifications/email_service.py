import smtplib
from email.mime.text import MIMEText

from app.notifications.config import *

class EmailService:

    @staticmethod
    def send(subject, body, receiver):

        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            receiver,
            msg.as_string()
        )

        server.quit()