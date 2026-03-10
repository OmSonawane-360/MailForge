import smtplib
from email.mime.text import MIMEText


def send_email(sender_email, app_password, receiver_email, subject, body):

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender_email, app_password)

        server.sendmail(sender_email, receiver_email, msg.as_string())

        server.quit()

        return True

    except Exception as e:
        print("Email failed:", e)
        return False