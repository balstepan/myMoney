from django import forms
from . import models
from django.contrib.auth.models import User


class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('name', 'balance')


class CostCategoryForm(forms.ModelForm):
    class Meta:
        model = models.CostCategory
        fields = ('name', 'parent')


class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = models.IncomeCategory
        fields = ('name',)


class CostForm(forms.ModelForm):
    class Meta:
        model = models.Cost
        fields = ('category', 'note', 'value', 'currency', 'account')


class IncomeForm(forms.ModelForm):
    class Meta:
        model = models.Income
        fields = ('category', 'note', 'value', 'currency', 'account')


class TransferForm(forms.ModelForm):
    class Meta:
        model = models.Transfer
        fields = ('from_account', 'to_account', 'value_from')
