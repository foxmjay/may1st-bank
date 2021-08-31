from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta


class Parameter(models.Model):
    cotisation_amount = models.DecimalField(max_digits=7, decimal_places=2, blank=False, default=500)
    start_date = models.DateField(editable=True)

    @staticmethod
    def supposedAmount():
        base = date.today()
        base = base.replace(day=1)
        parameter = Parameter.objects.first()
        months = relativedelta(base, parameter.start_date)
        months = months.years*12 + months.months+1
        return months * parameter.cotisation_amount
