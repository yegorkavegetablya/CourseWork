from django.shortcuts import render
from django.http import HttpResponse
from course_work.currency_predictions import create_prediction_plot


# Create your views here.
def give_currency_prediction(request, days_number):
    if days_number <= 30:
        context = {
            'days_number': days_number,
            'file_name': create_prediction_plot(days_number)
        }
        return render(request, 'plot_show.html', context)
    else:
        return HttpResponse("Ошибка: слишком большое число дней, доступно не больше 30")