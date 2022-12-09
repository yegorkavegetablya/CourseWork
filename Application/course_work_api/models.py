from django.db import models


# Create your models here.
class CurrencyPrediction:
    def __init__(self, status, result_message):
        self.status = status
        self.result_message = result_message
