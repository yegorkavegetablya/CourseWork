import requests
import json
from course_work.constants import JSON_RESULT_STRING
from scipy.interpolate import UnivariateSpline


def get_currency_information(days_number):
    query = "https://api.apilayer.com/currency_data/timeframe?"
    query += "start_date=2022-01-01"
    query += "&"
    query += "end_date=2022-03-01"
    query += "&"
    query += "currencies=DKK"
    query += "&"
    query += "source=RUB"
    query += "&"
    query += "apikey=ihujB93OoO8qFGK9mLXr1mdnNP8OxDtE"

    #response = requests.get(query)
    #print("\n\n\n\n\n", response.text, "\n\n\n\n\n", sep="")

    # return response.text
    return JSON_RESULT_STRING


def parse_json_result_string(string=JSON_RESULT_STRING):
    currency_information = json.loads(string)

    result = dict()
    for key in currency_information['quotes'].keys():
        result[key] = currency_information['quotes'][key]['RUBDKK']

    return result


def predict_values(days_number):
    data = get_currency_information(days_number)
    currency_information = parse_json_result_string(data)

    x = list([i + 1 for i in range(len(currency_information))])
    y = list(currency_information.values())
    spl = UnivariateSpline(x, y)

    result = []
    for i in range(days_number):
        new_value = float(spl(i + len(currency_information)))
        result.append(new_value)

    return result
