from django.contrib import admin
from .models import Subscriber, Newsletter  # Importing Subscriber and Newsletter models

# Function to send newsletters to all subscribers
def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)

# Setting a short description for the action
send_newsletter.short_description = "Send selected Newsletters to all subscribers"

# Customizing NewsletterAdmin to include the send_newsletter action
class NewsletterAdmin(admin.ModelAdmin):
    actions = [send_newsletter]

# Registering models with their respective admins
admin.site.register(Subscriber)  # Registering Subscriber model
admin.site.register(Newsletter, NewsletterAdmin)  # Registering Newsletter model with customized admin
