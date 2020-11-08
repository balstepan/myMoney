from django import forms
from . import models
from django.contrib.auth.models import User


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
