from django.db import models
from django.contrib.auth.models import User

# UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    minimum_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    enable_minimum_balance = models.BooleanField(default=False)

