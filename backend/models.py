# myapp/models.py
from django.db import models

class Inconsistency(models.Model):
    detail = models.CharField(max_length=255)

class Error(models.Model):
    message = models.CharField(max_length=255)

class Reachability(models.Model):
    status = models.CharField(max_length=255)

class RegisteredUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
