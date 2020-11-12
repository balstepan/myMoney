from decimal import Decimal
import requests
from datetime import datetime, timedelta
from django.utils import timezone

from . import models


def get_rates():
    cur_rates = models.Rates.objects.last() or models.Rates(usd=Decimal(2.5551), eur=Decimal(3.0184), rub=Decimal(0.0335),
                                                            updated_at=timezone.now() - timedelta(days=3))
    if cur_rates.updated_at < timezone.now() - timedelta(days=1):
        response = requests.get('https://www.nbrb.by/api/exrates/rates?periodicity=0')
        if response.ok:
            lst = response.json()
            usd = lst[4]['Cur_OfficialRate']
            eur = lst[5]['Cur_OfficialRate']
            rub = lst[16]['Cur_OfficialRate'] / lst[16]['Cur_Scale']
            cur_rates = models.Rates(usd=usd, eur=eur, rub=rub)
            cur_rates.save()
    return cur_rates


def get_byn(value, currency):
    if currency == 'BYN':
        return value
    else:
        return round(value * getattr(get_rates(), currency.lower()), 2)
