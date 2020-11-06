from django import forms
from . import models
from django.contrib.auth.models import User


class CostCategoryForm(forms.ModelForm):
    class Meta:
        model = models.CostCategory
        fields = ('name', 'parent')


class CostForm(forms.ModelForm):
    class Meta:
        model = models.Cost
        fields = ('category', 'note', 'value', 'currency', 'account')
