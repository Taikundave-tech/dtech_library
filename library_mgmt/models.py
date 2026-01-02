from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone

# [cite: 39] User Registration and Authentication
class User(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('LECTURER', 'Lecturer'),
        ('STAFF', 'Library Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

#  Resource Entity
class Resource(models.Model):
    RESOURCE_TYPES = (
        ('BOOK', 'Book'),
        ('COMPUTER', 'Computer Station'),
        ('SEAT', 'Study Seat'),
    )
    name = models.CharField(max_length=100) # e.g., "PC-01" or "Seat 45"
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"

# [cite: 41, 42] Session Logic (4-hour allocation)
class LibrarySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Only on create
            # Automate 4 hour session limit [cite: 42]
            self.end_time = timezone.now() + timedelta(hours=4)
        super().save(*args, **kwargs)

# [cite: 43] Resource Reservation
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class Book(models.Model):  # <--- MUST BE EXACTLY 'Book'
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)

