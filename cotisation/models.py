from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from parameter.models import Parameter
from datetime import date
from dateutil.relativedelta import relativedelta


class Cotisation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user", null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0)
    month = models.DateField(editable=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_by", null=True)
    created_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def amountSum(collections):
        amount = collections.aggregate(Sum('amount'))['amount__sum']
        if amount:
            return amount
        else:
            return 0
