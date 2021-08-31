from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    start_date = serializers.DateField(label='Date initiale', input_formats=['%d-%m-%Y'], format='%d-%m-%Y', required=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'amount', 'start_date']
