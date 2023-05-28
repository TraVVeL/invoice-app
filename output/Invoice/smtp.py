# -*- coding: utf-8 -*-
"""
Created : 08.05.2023

@author: --
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email_with_attachment(sender_email, sender_password, recipient_email, subject, message, file_path):
    # Создаем сообщение с заголовком и телом
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    body = MIMEText(message)
    msg.attach(body)

    # Открываем файл и создаем объект MIMEApplication
    with open(file_path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=file_path.split('/')[-1])
        msg.attach(attachment)

    # Инициализируем SMTP-клиент и отправляем сообщение
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

    print(f"Email sent to {recipient_email} with attachment {file_path} successfully.")
