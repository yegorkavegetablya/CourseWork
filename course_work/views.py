from django.shortcuts import render
from django.http import HttpResponse
from course_work.currency_predictions import get_currency_information


# Create your views here.
def give_currency_prediction(request, a):
    return HttpResponse(f"{get_currency_information(a)}")