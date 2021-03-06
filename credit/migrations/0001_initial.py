# Generated by Django 3.2.4 on 2021-06-29 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7)),
                ('cotisation_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('months', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('inprogress', 'En progrès'), ('ended', 'Termine')], default='inprogress', max_length=20)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credit_created_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cedit_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
