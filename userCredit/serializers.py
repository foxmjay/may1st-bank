
from .models import Credit
from rest_framework import serializers
from django.contrib.auth.models import User
from credit.models import Credit
from .models import UserCredit
from cotisation.serializers import UserSerializer


class UserCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredit
        fields = ['id', 'user', 'credit', 'amount', 'month', 'created_by']

    def create(self, validated_data):

        credit = validated_data['credit']
        validated_data['amount'] = credit.cotisation_amount
        validated_data['user'] = credit.user
        validated_data['created_by'] = User.objects.get(pk=1)
        return UserCredit.objects.create(**validated_data)


class UserCreditSerializerList(serializers.ModelSerializer):

    user = UserSerializer(many=False, read_only=True)
    created_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserCredit
        fields = ['id', 'user', 'amount', 'month', 'created_by']


class UserCreditSimplified:
    def __init__(self, date, cotisation):
        self.date = date
        self.cotisation = cotisation


class UserCreditSimplifiedSerializer(serializers.Serializer):
    date = serializers.DateField()
    cotisation = UserCreditSerializerList(many=False, read_only=True)

    class Meta:
        fields = ['date', 'cotisation']
