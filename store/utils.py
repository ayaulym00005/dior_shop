# store/utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_sms_via_email(phone_number, message):
    # Укажите информацию для вашего SMTP сервера
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    email_address = 'your_email@gmail.com'  # Замените на ваш email
    email_password = 'your_email_password'  # Замените на ваш пароль или используйте app-specific password

    # Укажите email-адрес для отправки SMS (для большинства операторов это будет такой формат: номер_телефона@оператор.com)
    sms_gateway = f'{phone_number}@sms.gateway.com'  # Замените на правильный шлюз оператора

    # Настройка MIME для email
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = sms_gateway
    msg['Subject'] = 'SMS via Email'

    # Тело письма с вашим сообщением
    body = MIMEText(message, 'plain')
    msg.attach(body)

    # Отправка email через SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Защищенное соединение
        server.login(email_address, email_password)
        text = msg.as_string()
        server.sendmail(email_address, sms_gateway, text)
        server.quit()
        print("SMS отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке SMS: {e}")
