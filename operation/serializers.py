from rest_framework import serializers


class OperationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    sumAmount = serializers.DecimalField(max_digits=7, decimal_places=2)
    creditLeft = serializers.DecimalField(max_digits=7, decimal_places=2)
    amountLeft = serializers.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        fields = ['id', 'first_name', 'last_name', 'sumAmount', 'creditLeft', 'amountLeft']


class GlobalStatsSerializer(serializers.Serializer):
    title = serializers.CharField()
    data = serializers.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        fields = ['title', 'data']
