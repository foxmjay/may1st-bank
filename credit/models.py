from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from parameter.models import Parameter
from datetime import date
from dateutil.relativedelta import relativedelta


class Credit(models.Model):
    STATUS = (('inprogress', 'En progrès'), ('ended', 'Termine'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="cedit_user", null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0)
    cotisation_amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0)
    start_date = models.DateField(editable=True)
    end_date = models.DateField(editable=True)
    months = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="credit_created_by", null=True)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, max_length=20, default='inprogress')
