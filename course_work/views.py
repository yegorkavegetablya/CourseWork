from django.shortcuts import render
from django.http import HttpResponse
from course_work.currency_predictions import create_prediction_plot


# Create your views here.
def give_currency_prediction(request, days_number):
    if days_number <= 30:
        return HttpResponse(f"{create_prediction_plot(days_number)}")
    else:
        return HttpResponse("Ошибка: слишком большое число дней, доступно не больше 30")