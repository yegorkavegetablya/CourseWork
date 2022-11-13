from rest_framework import serializers


class CurrencyPredictionSerializer(serializers.Serializer):
    status = serializers.CharField()
    result_message = serializers.CharField()
