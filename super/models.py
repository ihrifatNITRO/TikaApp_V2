# super/models.py

from django.db import models
from django.contrib.auth.models import User

class Child(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    child_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    next_vaccine_date = models.DateField(blank=True, null=True)
    taken_vaccines_list = models.TextField(blank=True, help_text="Enter vaccine names, separated by commas.")

    def __str__(self):
        return f"{self.child_name} (Child of {self.parent.email})"