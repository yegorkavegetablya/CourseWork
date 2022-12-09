import json

from django.urls import reverse
from rest_framework.test import APITestCase
import datetime


# Create your tests here.
class CurrencyPredictionAPITests(APITestCase):
    def test_result_ok(self):
        ideal_result = dict()
        ideal_result["status"] = "ok"
        ideal_result["result_message"] = "plot_"
        with open(f"./media/index.txt", 'r') as f:
            ideal_result["result_message"] += f.read()
        ideal_result["result_message"] += ".png"

        first_parameter = datetime.datetime.now() + datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=11)
        with open(f"./media/users.json", 'r') as f:
            third_parameter = json.load(f)["user_0"]

        url = reverse("predict_currency_api")
        response = self.client.get(url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}&api_key={third_parameter}")
        self.assertEqual(response.data, ideal_result)

    def test_result_error_wrong_api_key(self):
        ideal_result = dict()
        ideal_result["status"] = "error"
        ideal_result["result_message"] = "Ошибка, неверный API-ключ!"

        first_parameter = datetime.datetime.now() + datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=11)
        third_parameter = "!"

        url = reverse("predict_currency_api")
        response = self.client.get(url + f"?start_date={first_parameter.strftime('%d%m%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}&api_key={third_parameter}")
        self.assertEqual(response.data, ideal_result)

    def test_result_error_wrong_format_first(self):
        ideal_result = dict()
        ideal_result["status"] = "error"
        ideal_result["result_message"] = "Ошибка с первой датой: Неверный формат данных! Дата должна отображаться в виде дд-мм-гггг!"

        first_parameter = datetime.datetime.now() + datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=11)
        with open(f"./media/users.json", 'r') as f:
            third_parameter = json.load(f)["user_0"]

        url = reverse("predict_currency_api")
        response = self.client.get(url + f"?start_date={first_parameter.strftime('%d%m%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}&api_key={third_parameter}")
        self.assertEqual(response.data, ideal_result)

    def test_result_error_wrong_format_second(self):
        ideal_result = dict()
        ideal_result["status"] = "error"
        ideal_result["result_message"] = "Ошибка со второй датой: Неверный формат данных! Дата должна отображаться в виде дд-мм-гггг!"

        first_parameter = datetime.datetime.now() + datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=11)
        with open(f"./media/users.json", 'r') as f:
            third_parameter = json.load(f)["user_0"]

        url = reverse("predict_currency_api")
        response = self.client.get(url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d%m%Y')}&api_key={third_parameter}")
        self.assertEqual(response.data, ideal_result)

    def test_result_error_old_first(self):
        ideal_result = dict()
        ideal_result["status"] = "error"
        ideal_result["result_message"] = "Ошибка с первой датой: Дата уже наступила!"

        first_parameter = datetime.datetime.now() - datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=11)
        with open(f"./media/users.json", 'r') as f:
            third_parameter = json.load(f)["user_0"]

        url = reverse("predict_currency_api")
        response = self.client.get(url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}&api_key={third_parameter}")
        self.assertEqual(response.data, ideal_result)

    def test_result_error_old_second(self):
        ideal_result = dict()
        ideal_result["status"] = "error"
        ideal_result["result_message"] = "Ошибка со второй датой: Дата уже наступила!"

        first_parameter = datetime.datetime.now() + datetime.timedelta(days=11)
        second_parameter = datetime.datetime.now() - datetime.timedelta(days=1)
        with open(f"./media/users.json", 'r') as f:
            third_parameter = json.load(f)["user_0"]

        url = reverse("predict_currency_api")
        response = self.client.get(url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}&api_key={third_parameter}")
        self.assertEqual(response.data, ideal_result)

    def test_result_error_second_later(self):
        ideal_result = dict()
        ideal_result["status"] = "error"
        ideal_result["result_message"] = "Ошибка, начальная дата не может быть позже конечной!"

        first_parameter = datetime.datetime.now() + datetime.timedelta(days=11)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=1)
        with open(f"./media/users.json", 'r') as f:
            third_parameter = json.load(f)["user_0"]

        url = reverse("predict_currency_api")
        response = self.client.get(url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}&api_key={third_parameter}")
        self.assertEqual(response.data, ideal_result)

    def test_result_error_out_of_interval(self):
        ideal_result = dict()
        ideal_result["status"] = "error"
        ideal_result["result_message"] = "Ошибка, дата выходит за пределы допустимого интервала предсказания, доступны следующие 200 дней!"

        first_parameter = datetime.datetime.now() + datetime.timedelta(days=1)
        second_parameter = datetime.datetime.now() + datetime.timedelta(days=201)
        with open(f"./media/users.json", 'r') as f:
            third_parameter = json.load(f)["user_0"]

        url = reverse("predict_currency_api")
        response = self.client.get(url + f"?start_date={first_parameter.strftime('%d-%m-%Y')}&end_date={second_parameter.strftime('%d-%m-%Y')}&api_key={third_parameter}")
        self.assertEqual(response.data, ideal_result)
