from src.email_services import *


def compose_email_for_recipient(email_recipient: str, body: str, subject: str) -> EmailMessage:
    global EMAIL_SENDER  # get the global variable of sender
    em = EmailMessage()
    em['From'] = EMAIL_SENDER
    em['To'] = email_recipient
    em['Subject'] = subject
    em.set_content(body)
    em.add_alternative(body, subtype='html')
    return em


def send_mail_to_single_recipient(context, email_message: EmailMessage, email_recipient: str) -> None:
    global EMAIL_SENDER, EMAIL_PASSWORD
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, email_recipient, email_message.as_string())
        print(f"Mail sent successfully to recipient: {email_recipient} :)")


def send_mail_to_all_recipients(email_recipients: list[str], body: str, subject: str) -> None:
    context = ssl.create_default_context()

    for email_recipient in email_recipients:
        print(f"Sending message to {email_recipient}")
        em = compose_email_for_recipient(email_recipient, body=body, subject=subject)
        send_mail_to_single_recipient(context, email_message=em, email_recipient=email_recipient)


if __name__ == '__main__':
    recps = ['maximmu87@gmail.com', 'maximmu87@gmail.com']
    subject = "Hello there mate!"
    send_mail_to_all_recipients(recps, body="<h1>TEST</h1>", subject="TEST")
