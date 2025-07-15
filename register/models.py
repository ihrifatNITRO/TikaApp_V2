from encodings.punycode import T
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # This links each Profile to exactly one User.
    # If a User is deleted, their Profile will be deleted too.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # extra, custom fields
    id_card = models.IntegerField(unique=True)
    phone_number = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.user.username} Profile'