import datetime

from django.shortcuts import render
from django.http import HttpResponse
from course_work.currency_predictions import create_prediction_plot


# Create your views here.
def give_currency_prediction(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date_result = check_date(start_date)
    end_date_result = check_date(end_date)

    if isinstance(start_date_result, str):
        return HttpResponse("Ошибка с первой датой: " + start_date_result)
    if isinstance(end_date_result, str):
        return HttpResponse("Ошибка со второй датой: " + end_date_result)

    if start_date_result > end_date_result:
        return HttpResponse("Ошибка, начальная дата не может быть позже конечной!")

    if datetime.datetime.now() + datetime.timedelta(days=200) < end_date_result:
        return HttpResponse("Ошибка, дата выходит за пределы допустимого интервала предсказания, доступны следующие 200 дней!")

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'file_name': create_prediction_plot(start_date_result, end_date_result)
    }
    return render(request, 'plot_show.html', context)


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


def testing_view(request):
    return HttpResponse("Тестовый ответ")
