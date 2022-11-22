from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Example 1",
            summary="Response code is 200, programme maintained the request",
            description="Everything is fine",
            value={
                "status": "ok",
                "result_message": "plot_0.png"
            }
        ),
        OpenApiExample(
            "Example 2",
            summary="Response code is 200, programme maintained the request",
            description="Error occurred (parameters format or value is wrong)",
            value={
                'status': "error",
                "result_message": "Неверный формат данных! Дата должна отображаться в виде дд-мм-гггг!"
            }
        )
    ]
)
class CurrencyPredictionSerializer(serializers.Serializer):
    status = serializers.CharField()
    result_message = serializers.CharField()
