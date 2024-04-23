from django.db import models
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Define a model to represent subscribers
class Subscriber(models.Model):
    email = models.EmailField(unique=True)  # Field to store subscriber email address

    # String representation of the Subscriber object
    def __str__(self):
        return self.email

# Define a model to represent newsletters
class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time when the newsletter was created
    updated_at = models.DateTimeField(auto_now=True)  # Date and time when the newsletter was last updated
    subject = models.CharField(max_length=150)  # Subject of the newsletter
    contents = models.FileField(upload_to='uploaded_newsletters/')  # Field to upload the contents of the newsletter

    # String representation of the Newsletter object
    def __str__(self):
        # Concatenating subject and creation date for a meaningful representation
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    # Method to send the newsletter to subscribers
    def send(self, request):
        # Read the contents of the newsletter file
        contents = self.contents.read().decode('utf-8')
        
        # Get all subscribers
        subscribers = Subscriber.objects.all()
        
        # Initialize SendGrid API client
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        
        # Iterate over subscribers and send the newsletter to each
        for sub in subscribers:
            # Construct the email message
            message = Mail(
                from_email=settings.FROM_EMAIL,  # Sender's email address
                to_emails=sub.email,  # Recipient's email address
                subject=self.subject,  # Subject of the email
                html_content=contents + (  # HTML content of the email
                    '<center><br><a href="{}?email={}">Unsubscribe</a>.').format(
                        request.build_absolute_uri('/delete/'),
                        sub.email
                    )
            )
            # Send the email message using SendGrid
            sg.send(message)
