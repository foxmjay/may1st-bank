from .models import Parameter
from rest_framework import serializers


class ParameterSerializer(serializers.HyperlinkedModelSerializer):

    start_date = serializers.DateField(label='Date initiale', input_formats=['%d-%m-%Y'], format='%d-%m-%Y', required=True)

    class Meta:
        model = Parameter
        fields = ['id', 'cotisation_amount', 'start_date']
