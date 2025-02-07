# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Itinerary(models.Model):
    """
    A simplified model to store travel itineraries.
    Combines title, destination, dates, activities, and expenses.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, null=True)
    title = models.CharField(max_length=255, help_text="Title of the itinerary")
    destination = models.CharField(max_length=255, help_text="Destination of the trip")
    start_date = models.DateField(help_text="Start date of the trip")
    end_date = models.DateField(help_text="End date of the trip")
    activities = models.TextField(blank=True, help_text="List of activities (comma-separated)")
    expenses = models.TextField(blank=True, help_text="List of expenses (comma-separated)")

    def __str__(self):
        """
        String representation of the itinerary.
        """
        return f"{self.title} - {self.destination} ({self.start_date} to {self.end_date})"

class CustomUser(AbstractUser):
    # Your custom fields here
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Modify related_name here
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Modify related_name here
        blank=True,
    )