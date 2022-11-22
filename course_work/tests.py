from django.test import TestCase
from django.urls import reverse
import datetime


# Create your tests here.
class CurrencyPredictionTests(TestCase):
    def test_result_ok(self):
        ideal_result = dict()
        ideal_result["start_date"] = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
        ideal_result["end_date"] = (datetime.datetime.now() + datetime.timedelta(days=11)).strftime("%d-%m-%Y")
        ideal_result["file_name"] = "plot_"
        with open(".\\media\\index.txt", 'r') as f:
            ideal_result["file_name"] += f.read()
        ideal_result["file_name"] += ".png"

        first_parameter = datetime.datetime.now() + datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=11)

        url = reverse("predict_currency")
        response = self.client.get(
            url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}")
        self.assertEqual(response.context.pop(), ideal_result)

    def test_result_error_wrong_format_first(self):
        first_parameter = datetime.datetime.now() + datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=11)

        url = reverse("predict_currency")
        response = self.client.get(
            url + f"?start_date={first_parameter.strftime('%d%m%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}")
        self.assertEqual(response.content.decode("utf-8"),
                         "Ошибка с первой датой: Неверный формат данных! Дата должна отображаться в виде дд-мм-гггг!")

    def test_result_error_wrong_format_second(self):
        first_parameter = datetime.datetime.now() + datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=11)

        url = reverse("predict_currency")
        response = self.client.get(
            url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d%m%Y')}")
        self.assertEqual(response.content.decode("utf-8"),
                         "Ошибка со второй датой: Неверный формат данных! Дата должна отображаться в виде дд-мм-гггг!")

    def test_result_error_old_first(self):
        first_parameter = datetime.datetime.now() - datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=11)

        url = reverse("predict_currency")
        response = self.client.get(
            url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}")
        self.assertEqual(response.content.decode("utf-8"), "Ошибка с первой датой: Дата уже наступила!")

    def test_result_error_old_second(self):
        first_parameter = datetime.datetime.now() + datetime.timedelta(days=11)
        second_parameter = datetime.datetime.now() - datetime.timedelta(days=1)

        url = reverse("predict_currency")
        response = self.client.get(
            url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}")
        self.assertEqual(response.content.decode("utf-8"), "Ошибка со второй датой: Дата уже наступила!")

    def test_result_error_second_later(self):
        first_parameter = datetime.datetime.now() + datetime.timedelta(days=11)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=1)

        url = reverse("predict_currency")
        response = self.client.get(
            url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}")
        self.assertEqual(response.content.decode("utf-8"), "Ошибка, начальная дата не может быть позже конечной!")

    def test_result_error_out_of_interval(self):
        first_parameter = datetime.datetime.now() + datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=201)

        url = reverse("predict_currency")
        response = self.client.get(
            url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}")
        self.assertEqual(response.content.decode("utf-8"),
                         "Ошибка, дата выходит за пределы допустимого интервала предсказания, доступны следующие 200 дней!")