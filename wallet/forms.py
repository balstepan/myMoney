from django import forms
from django.views.generic import FormView

from . import models
from django.contrib.auth.models import User


class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('name', 'balance', 'image')


class CostCategoryForm(forms.ModelForm):
    class Meta:
        model = models.CostCategory
        fields = ('name', 'parent', 'image')

    def __init__(self, user, *args, **kwargs):
        super(CostCategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = models.CostCategory.objects.filter(user=user)


class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = models.IncomeCategory
        fields = ('name', 'image')


class CostForm(forms.ModelForm):
    class Meta:
        model = models.Cost
        fields = ('category', 'note', 'value', 'currency', 'account')

    def __init__(self, user, *args, **kwargs):
        super(CostForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = models.CostCategory.objects.filter(user=user)
        self.fields['account'].queryset = models.Account.objects.filter(user=user)


class IncomeForm(forms.ModelForm):
    class Meta:
        model = models.Income
        fields = ('category', 'note', 'value', 'currency', 'account')

    def __init__(self, user, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = models.IncomeCategory.objects.filter(user=user)
        self.fields['account'].queryset = models.Account.objects.filter(user=user)


class TransferForm(forms.ModelForm):
    class Meta:
        model = models.Transfer
        fields = ('from_account', 'to_account', 'value_from')

    def __init__(self, user, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].queryset = models.Account.objects.filter(user=user)
        self.fields['to_account'].queryset = models.Account.objects.filter(user=user)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                               widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('bad password')
        return cd['password']
