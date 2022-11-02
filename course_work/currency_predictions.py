import requests


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
    #print(response.text)
    # return response.text
    return "!"