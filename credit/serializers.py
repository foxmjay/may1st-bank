
from .models import Credit
from rest_framework import serializers
from django.contrib.auth.models import User
from cotisation.serializers import UserSerializer


class CreditSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(label='Date initiale', input_formats=['%d-%m-%Y'], format='%d-%m-%Y', required=True)
    end_date = serializers.DateField(label='Date initiale', input_formats=['%d-%m-%Y'], format='%d-%m-%Y', required=True)

    class Meta:
        model = Credit
        fields = ['id', 'user', 'amount', 'cotisation_amount', 'start_date', 'end_date', 'months', 'created_by', 'status']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return Credit.objects.create(**validated_data)


class CreditSerializerList(serializers.ModelSerializer):

    start_date = serializers.DateField(label='Date initiale', input_formats=['%d-%m-%Y'], format='%d-%m-%Y', required=True)
    end_date = serializers.DateField(label='Date initiale', input_formats=['%d-%m-%Y'], format='%d-%m-%Y', required=True)
    user = UserSerializer(many=False, read_only=True)
    created_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Credit
        fields = ['id', 'user', 'amount', 'cotisation_amount', 'start_date', 'end_date', 'months', 'created_by', 'status']
