import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail
from django.conf import settings

class MockResponse(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def send(email_model):
    sg = sendgrid.SendGridAPIClient(apikey=email_model.provider.apikey)
    from_email = Email(email_model.from_email)
    to_emails = [Email(e) for e in email_model.to_emails]
    content = Content(email_model.content_type, email_model.rendered)
    subject = email_model.subject

    mail = Mail(from_email, subject, to_emails[0], content)
    for email in range(1, len(to_emails)):
        mail.personalizations[0].add(email)
    # TODO need to insert custom arg for the id
    # TODO is there a better way?
    if settings.TESTING:
        return MockResponse(status_code=202)
    else:
        return sg.client.mail.send.post(request_body=mail.get())
