from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CurrencyPrediction, ImageFromPillow
from .serializers import CurrencyPredictionSerializer, ImageFromPillowSerializer
from course_work.currency_predictions import create_prediction_plot, encode_image
import datetime
import json
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


# Create your views here.
class CurrencyPredictionView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="start_date",
                description="date by which the prediction interval starts",
                required=True,
                type=OpenApiTypes.DATE
            ),
            OpenApiParameter(
                name="end_date",
                description="date by which the prediction interval ends",
                required=True,
                type=OpenApiTypes.DATE
            ),
            OpenApiParameter(
                name="api_key",
                description="API key for authentication",
                required=True,
                type=OpenApiTypes.STR
            )
        ],
        description="Currency prediction for certain interval",
        responses={
            200: CurrencyPredictionSerializer
        },
        methods=["GET"]
    )
    def get(self, request):
        status = "ok"
        result_message = ""

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        api_key = request.GET.get('api_key')

        start_date_result = check_date(start_date)
        end_date_result = check_date(end_date)

        with open(f"./static/users.json", 'r') as f:
            users = json.load(f)

        if api_key not in users.values():
            status = 'error'
            result_message = "Ошибка, неверный API-ключ!"
        elif isinstance(start_date_result, str):
            status = "error"
            result_message = "Ошибка с первой датой: " + start_date_result
        elif isinstance(end_date_result, str):
            status = "error"
            result_message = "Ошибка со второй датой: " + end_date_result
        elif start_date_result > end_date_result:
            status = "error"
            result_message = "Ошибка, начальная дата не может быть позже конечной!"
        elif datetime.datetime.now() + datetime.timedelta(days=200) < end_date_result:
            status = "error"
            result_message = "Ошибка, дата выходит за пределы допустимого интервала предсказания, доступны следующие 200 дней!"
        else:
            result_message = create_prediction_plot(start_date_result, end_date_result)

        currency_prediction = CurrencyPrediction(status, result_message)

        currency_prediction_serializer = CurrencyPredictionSerializer(instance=currency_prediction)

        return Response(currency_prediction_serializer.data)


def check_date(str_date):
    if not isinstance(str_date, str):
        return "Тип данных должен быть строкой!"

    try:
        date_date = datetime.datetime.strptime(str_date, "%d-%m-%Y")
    except ValueError:
        return "Неверный формат данных! Дата должна отображаться в виде дд-мм-гггг!"

    if datetime.datetime.now() > date_date:
        return "Дата уже наступила!"

    return date_date


class ImageFromPillowView(APIView):
    def get(self, request, name):
        image_string = encode_image(f'./static/' + name)
        image_result = ImageFromPillow(image_string, 'utf-8')
        serializer_for_request = ImageFromPillowSerializer(instance=image_result)

        return Response(serializer_for_request.data)
