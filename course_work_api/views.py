from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CurrencyPrediction
from .serializers import CurrencyPredictionSerializer
from course_work.currency_predictions import create_prediction_plot
import datetime
import json


# Create your views here.
class CurrencyPredictionView(APIView):
    def get(self, request):
        status = "ok"
        result_message = ""

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        api_key = request.GET.get('api_key')

        start_date_result = check_date(start_date)
        end_date_result = check_date(end_date)

        with open(".\\media\\users.json", 'r') as f:
            users = json.load(f)
        if api_key not in users.values():
            status = 'error'
            result_message = "Ошибка, неверный API-ключ!"

        if isinstance(start_date_result, str):
            status = "error"
            result_message = "Ошибка с первой датой: " + start_date_result
        if isinstance(end_date_result, str):
            status = "error"
            result_message = "Ошибка со второй датой: " + end_date_result

        if start_date_result > end_date_result:
            status = "error"
            result_message = "Ошибка, начальная дата не может быть позже конечной!"

        if datetime.datetime.now() + datetime.timedelta(days=200) < end_date_result:
            status = "error"
            result_message = "Ошибка, дата выходит за пределы допустимого интервала предсказания, доступны следующие 200 дней!"

        if status == "ok":
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
