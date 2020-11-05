from django import forms
from . import models
from django.contrib.auth.models import User


class CostCategoryForm(forms.ModelForm):
    class Meta:
        model = models.CostCategory
        fields = ('name', 'parent')
