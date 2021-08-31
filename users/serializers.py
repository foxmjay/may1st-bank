from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import hashers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'date_joined']


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'date_joined']

    def create(self, validated_data):
        validated_data['password'] = hashers.make_password(validated_data['password'])
        return User.objects.create(**validated_data)
