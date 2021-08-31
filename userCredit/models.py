from django.db import models
from django.contrib.auth.models import User
from parameter.models import Parameter
from datetime import date
from dateutil.relativedelta import relativedelta
from credit.models import Credit


class UserCredit(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="credituser_user", null=True)
    credit = models.ForeignKey(Credit, on_delete=models.SET_NULL, related_name="credituser_credit", null=True)
    month = models.DateField(editable=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="userCredit_created_by", null=True)
    created_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def amountSum(collections):
        return collections.aggregate(Sum('amount'))['amount__sum']
