from .models import Cotisation
from rest_framework import serializers
from django.contrib.auth import hashers
from django.contrib.auth.models import User
from cotisation.models import Cotisation
from userProfile.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class CotisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotisation
        fields = ['id', 'user', 'amount', 'month', 'created_by']

    def create(self, validated_data):
        userProfile = UserProfile.objects.get(user__id=validated_data['user'].id)
        validated_data['amount'] = userProfile.amount
        validated_data['created_by'] = User.objects.get(pk=1)
        return Cotisation.objects.create(**validated_data)


class CotisationSerializerList(serializers.ModelSerializer):

    user = UserSerializer(many=False, read_only=True)
    created_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Cotisation
        fields = ['id', 'user', 'amount', 'month', 'created_by']


class CotisationSimplified:
    def __init__(self, date, cotisation):
        self.date = date
        self.cotisation = cotisation


class CotisationSimplifiedSerializer(serializers.Serializer):
    date = serializers.DateField()
    cotisation = CotisationSerializerList(many=False, read_only=True)

    class Meta:
        fields = ['date', 'cotisation']
