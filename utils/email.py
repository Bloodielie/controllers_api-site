from configuration.config import login_email, password_email
from typing import Union
import re

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart()
msg['From'] = login_email
msg['Subject'] = 'Аунтефикация!!!'


def send_email(addr_to, url_authentication) -> None:
    server_email = smtplib.SMTP('smtp.gmail.com', 587)
    server_email.starttls()
    msg['To'] = addr_to
    body = url_authentication
    msg.attach(MIMEText(body, 'plain'))
    server_email.send_message(msg)
    server_email.quit()


def email_validation(address) -> Union[None, str]:
    pattern = re.compile(r'^(\w+)@(\w+\.\w+)$')
    is_valid = pattern.match(address)
    if is_valid:
        return address
    return None
