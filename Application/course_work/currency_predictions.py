import base64
import requests
import json
from course_work.constants import API_KEY, JSON_RESULT_STRING
from scipy.interpolate import UnivariateSpline
import datetime
import seaborn
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as p


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

    response = requests.get(query)

    return response.text


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

    dataFrame = p.DataFrame([[dates[i], data[i], 0] for i in range(len(dates))],
                    columns=["Дата", "Значение по отношению к рублю", "Кривая курса валют"])

    seaborn.set_theme(style="darkgrid")
    rcParams['figure.figsize'] = 20, 10
    plt.fill_between(dates, data, min(data), facecolor="red", color="yellow", alpha=0.5)
    for i in range(len(dates)):
        min_y = 0.05
        max_y = 0.05 + ((data[i] - min(data)) / (max(data) - min(data))) / 100 * 90
        plt.axvline(dates[i], min_y, max_y, color="orange", linestyle="dashed")
    seaborn.lineplot(dataFrame, x="Дата", y="Значение по отношению к рублю", color="red",
                     dashes=True, markers=True, style="Кривая курса валют")
    plt.xticks(rotation=40)
    plt.title(f"Предсказание курса валют датской кроны с {start_date_result.strftime('%d-%m-%Y')} по {end_date_result.strftime('%d-%m-%Y')}")

    return save_plot()


def save_plot():
    current_index = -1
    with open(f"./static/index.txt", 'r') as fi:
        current_index = int(fi.read())
    with open(f"./static/index.txt", 'w') as fo:
        fo.write(str(current_index + 1))

    file_name = "plot_" + str(current_index) + ".png"
    plt.savefig(f"./static/" + file_name)

    return file_name


def encode_image(image_path):
    with open(image_path, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')

        return base64_message
