from app.configuration.config import LOGIN_EMAIL, PASSWORD_EMAIL
from typing import Union
import re

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    @classmethod
    def send_email(cls, addr_to: str, url_authentication: str) -> None:
        server_email = smtplib.SMTP('smtp.gmail.com', 587)
        server_email.starttls()
        server_email.login(LOGIN_EMAIL, PASSWORD_EMAIL)

        msg = MIMEMultipart()
        msg['From'] = LOGIN_EMAIL
        msg['To'] = addr_to
        msg['Subject'] = 'Аунтефикация!!!'
        body = url_authentication
        msg.attach(MIMEText(body, 'plain'))

        server_email.send_message(msg)
        server_email.quit()

    @staticmethod
    def email_validation(address: str) -> Union[None, str]:
        pattern = re.compile(r'^(\w+)@(\w+\.\w+)$')
        is_valid = pattern.match(address)
        if is_valid:
            return address
        return None
