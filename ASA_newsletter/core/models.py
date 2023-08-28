from django.db import models
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.email 
    

class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='uploaded_newsletters/')

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")
    

    def send(self, request):
            contents = self.contents.read().decode('utf-8')
            subscribers = Subscriber.objects.filter()
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            for sub in subscribers:
                message = Mail(
                        from_email=settings.FROM_EMAIL,
                        to_emails=sub.email,
                        subject=self.subject,
                        html_content=contents + (
                            '<center><br><a href="{}?email={}">Unsubscribe</a>.').format(
                                request.build_absolute_uri('/delete/'),
                                sub.email
                                ))
                sg.send(message)