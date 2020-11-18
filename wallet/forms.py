from django import forms
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


class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = models.IncomeCategory
        fields = ('name', 'image', 'image')


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
