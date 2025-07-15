# super/admin.py

from django.contrib import admin
from .models import Child # Import the Child model

# This line tells the admin site to display the Child model
admin.site.register(Child)