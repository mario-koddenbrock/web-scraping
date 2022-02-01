import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(
    subject="News from RaspberryPi",
    body="Just an email from the Python.",
    to="koddenbrock@gmail.com"  # to=["koddenbrock@gmail.com", "hasensilvester@gmail.com"]
):

    if isinstance(to, list):
        for receiver in to:
            send_mail(subject=subject, body=body, to=receiver)
        return

    gmail_user = "projectdatascience22@gmail.com"
    gmail_password = "B3fjfF9XkyayAJG"
    sent_from = gmail_user
    to = 'koddenbrock@gmail.com'

    message = MIMEMultipart()
    message['From'] = sent_from
    message['To'] = to
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # server.ehlo()
        # server.login(gmail_user, gmail_password)
        # server.sendmail(sent_from, to, message.as_string())
        # server.close()

        print('Email sent!')
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


# send_mail("Test Mail", "Hallo Christoph! \nWir haben jetzt eine Mail-Adresse fürs Projekt und können uns so benachrichtigen, wenn was mit dem Server nicht stimmt.\n Diese Nachricht hier kommt also direkt aus Python\nYeah!")
