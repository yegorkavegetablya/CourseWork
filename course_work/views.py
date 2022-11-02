from django.shortcuts import render
from django.http import HttpResponse
from course_work.currency_predictions import predict_values


# Create your views here.
def give_currency_prediction(request, a):
    return HttpResponse(f"{predict_values(a)}")