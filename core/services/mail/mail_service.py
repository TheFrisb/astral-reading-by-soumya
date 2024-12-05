from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Content


class MailService:
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.default_from_mail = settings.DEFAULT_FROM_EMAIL
        self.client = SendGridAPIClient(self.api_key)

    def send_mail(self, to_email, subject, content):
        from_email = From(self.default_from_mail)
        to_email = To(to_email)
        content = Content("text/plain", content)
        mail = Mail(from_email, to_email, subject, content)

        response = self.client.send(mail)
        print(response.status_code)
        print(response.headers)
        print(response.body)

        return response
