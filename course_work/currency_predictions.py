import requests
import json
from course_work.constants import API_KEY, JSON_RESULT_STRING
from scipy.interpolate import UnivariateSpline
import datetime
import seaborn
import matplotlib.pyplot as plt
import time


def get_currency_information():
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d")
    then = now - datetime.timedelta(days=360)
    then_str = then.strftime("%Y-%m-%d")

    query = "https://api.apilayer.com/currency_data/timeframe?"
    query += ("start_date=" + then_str)
    query += "&"
    query += ("end_date=" + now_str)
    query += "&"
    query += "currencies=DKK"
    query += "&"
    query += "source=RUB"
    query += "&"
    query += f"apikey={API_KEY}"

    # response = requests.get(query)
    # print("\n\n\n\n\n", response.text, "\n\n\n\n\n", sep="")
    #
    # return response.text
    return JSON_RESULT_STRING


def parse_json_result_string(string=JSON_RESULT_STRING):
    currency_information = json.loads(string)

    result = dict()
    for key in currency_information['quotes'].keys():
        result[key] = currency_information['quotes'][key]['RUBDKK']

    return result


def predict_values(start_date_result, end_date_result):
    data = get_currency_information()
    currency_information = parse_json_result_string(data)

    x = list([i + 1 for i in range(len(currency_information))])
    y = list(currency_information.values())
    spl = UnivariateSpline(x, y)

    result = []
    difference = (start_date_result - datetime.datetime.now()).days
    for i in range((end_date_result - start_date_result).days + 1):
        new_value = float(spl(i + difference + len(currency_information)))
        result.append(new_value)

    return result


def create_prediction_plot(start_date_result, end_date_result):
    data = predict_values(start_date_result, end_date_result)
    dates = []

    start_date = start_date_result
    for i in range((end_date_result - start_date_result).days + 1):
        dates.append(start_date.strftime("%y/%m/%d"))
        start_date = start_date + datetime.timedelta(days=1)

    seaborn.lineplot(x=dates, y=data)
    plt.xticks(rotation=70)

    return save_plot()


def save_plot():
    current_index = -1
    with open(".\\media\\index.txt", 'r') as fi:
        current_index = int(fi.read())
    with open(".\\media\\index.txt", 'w') as fo:
        fo.write(str(current_index + 1))

    file_name = "plot_" + str(current_index) + ".png"
    plt.savefig(".\\media\\" + file_name)

    return file_name