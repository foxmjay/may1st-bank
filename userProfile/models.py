from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_userProfile", null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0)
    start_date = models.DateField(editable=True)
    created_at = models.DateTimeField(auto_now=True)
