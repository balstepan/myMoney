import requests
from datetime import datetime, timedelta

from . import models


def get_rates():
    try:
        rates = models.Rates.objects.last()
    except:
        rates = models.Rates.create(usd=2.5551, eur=3.0184, rub=0.0335, updated_at=datetime(year=1970, month=1, day=1))
    response = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
    if response.ok:
        lst = response.json()
        usd = lst[4]['Cur_OfficialRate']
        eur = lst[5]['Cur_OfficialRate']
        rub = lst[16]['Cur_OfficialRate'] / lst[16]['Cur_Scale']
        rates = models.Rates.create(usd=usd, eur=eur, rub=rub)
