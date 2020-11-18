import os
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from pytils.translit import slugify

from PIL import Image

from . import models
from . import forms
from . import rates
from myMoney.settings import (
    DEFAULT_ACCOUNTS, DEFAULT_COST_CATEGORIES, DEFAULT_INCOME_CATEGORIES,
    DEFAULT_ACCOUNTS_ICONS, DEFAULT_INCOME_ICONS, DEFAULT_COST_ICONS,
    ICON_SIZE)

class AllAccounts(LoginRequiredMixin, View):
    def get(self, request):
        accounts = models.Account.objects.filter(user=request.user)
        return render(request,
                      'accounts/all_accounts.html',
                      {'accounts': accounts})


class AccountDetail(LoginRequiredMixin, View):
    def get(self, request, user_id=None, slug=None):
        if slug:
            account = get_object_or_404(models.Account, slug=slug,
                                        user=get_object_or_404(models.User, pk=user_id))
            account_form = forms.AccountForm(instance=account)
        else:
            account_form = forms.AccountForm()
        return render(request,
                      'accounts/create.html',
                      {'form': account_form})

    def post(self, request, user_id=None, slug=None):
        if slug:
            account = models.Account.objects.get(user=get_object_or_404(models.User, pk=user_id),
                                                 slug=slug)
            account_form = forms.AccountForm(request.POST, instance=account, files=request.FILES)
            if not account_form['image']:
                account_form['image'] = account.image.name
        else:
            account_form = forms.AccountForm(request.POST, files=request.FILES)
        if account_form.is_valid():
            new_account = account_form.save(commit=False)
            new_account.user = request.user
            new_account.slug = slugify(new_account.name)
            new_account.save()
            if new_account.image:
                edit_image(new_account.image.path)
        return redirect('wallet:all_accounts')


@login_required
def account_delete(request, acc_id):
    account = get_object_or_404(models.Account, id=acc_id)

    if request.method == "POST":
        account.delete()
        return redirect("wallet:all_accounts")
    else:
        return render(request,
                      'delete.html',
                      {'obj_type': 'account',
                       'object': account})


class AllCostCategories(LoginRequiredMixin, View):

    def _get_all_children(self, parent_cat):
        cat_list = []
        if parent_cat.children.all():
            cat_list += list(parent_cat.children.all())
            for cat in parent_cat.children.all():
                cat_list += self._get_all_children(cat)
        return cat_list

    def get(self, request, days=30):
        cost_categories_list = models.CostCategory.objects.filter(parent=None,
                                                                  user=request.user)
        amounts = []
        for cat in cost_categories_list:
            cats_for_count = [cat, ] + self._get_all_children(cat)
            amount = 0
            for cat_for_count in cats_for_count:
                costs = cat_for_count.costs.filter(created_at__gt=datetime.now() - timedelta(days=days))
                for cost in costs:
                    amount += rates.get_byn(cost.value, cost.currency)
            amounts.append(amount)
        context = zip(cost_categories_list, amounts)
        return render(request,
                      'costCategories/all_categories.html',
                      {'categories': context})


class CostCategory(LoginRequiredMixin, View):

    def get(self, request, user_id, slug, days=30):
        category = get_object_or_404(models.CostCategory, slug=slug,
                                     user=get_object_or_404(models.User, pk=user_id))
        children = category.children.all()
        costs = category.costs.filter(created_at__gt=datetime.now()-timedelta(days=days)).order_by('-created_at')
        return render(request,
                      'costCategories/costcategory_detail.html',
                      {'category': category,
                       'children': children,
                       'costs': costs})


class CreateCostCategory(LoginRequiredMixin, View):
    def get(self, request, costcat_id=None):
        if costcat_id:
            cost_category = models.CostCategory.objects.get(pk=costcat_id)
            cost_category_form = forms.CostCategoryForm(instance=cost_category, user=request.user)
        else:
            cost_category_form = forms.CostCategoryForm(user=request.user)
        return render(request,
                      'costCategories/create.html',
                      {'form': cost_category_form})

    def post(self, request, costcat_id=None):
        if not costcat_id:
            cost_category_form = forms.CostCategoryForm(request.user, request.POST, files=request.FILES)
            if cost_category_form.is_valid():
                new_category = cost_category_form.save(commit=False)
                new_category.user = request.user
                new_category.slug = slugify(new_category.name)
                new_category.save()
                if new_category.image:
                    edit_image(new_category.image.path)
                return render(request,
                          'costCategories/costcategory_detail.html',
                          {'category': new_category})
        else:
            cost_category = models.CostCategory.objects.get(pk=costcat_id)
            cost_category_form = forms.CostCategoryForm(request.user, request.POST, instance=cost_category, files=request.FILES)
            if cost_category_form.is_valid():
                new_category = cost_category_form.save(commit=False)
                new_category.user = request.user
                new_category.slug = slugify(new_category.name)
                new_category.save()
                if new_category.image:
                    edit_image(new_category.image.path)
                return redirect(new_category)


@login_required()
def cost_category_delete(request, costcat_id):
    cost_category = get_object_or_404(models.CostCategory, id=costcat_id)

    if request.method == "POST":
        cost_category.delete()
        return redirect("wallet:all_cost_categories")
    else:
        return render(request,
                      'delete.html',
                      {'obj_type': 'cost category',
                       'object': cost_category})


class AllIncomeCategories(LoginRequiredMixin, View):

    def get(self, request, days=30):
        income_categories_list = models.IncomeCategory.objects.filter(user=request.user)
        amounts = []
        for cat in income_categories_list:
            incomes = cat.incomes.filter(created_at__gt=datetime.now() - timedelta(days=days))
            amount = 0
            for income in incomes:
                amount += rates.get_byn(income.value, income.currency)
            amounts.append(amount)
        context = zip(income_categories_list, amounts)
        return render(request,
                      'incomeCategories/all_categories.html',
                      {'categories': context})


class IncomeCategory(LoginRequiredMixin, View):

    def get(self, request, user_id, slug, days=30):
        category = get_object_or_404(models.IncomeCategory, slug=slug,
                                     user=get_object_or_404(models.User, pk=user_id))
        incomes = category.incomes.filter(created_at__gt=datetime.now()-timedelta(days=days)).order_by('-created_at')
        return render(request,
                      'incomeCategories/incomecategory_detail.html',
                      {'category': category,
                       'incomes': incomes})


@login_required
def income_category_delete(request, incomecat_id):
    income_category = get_object_or_404(models.IncomeCategory, id=incomecat_id)

    if request.method == "POST":
        income_category.delete()
        return redirect("wallet:all_income_categories")
    else:
        return render(request,
                      'delete.html',
                      {'obj_type': 'income category',
                       'object': income_category})


class CreateIncomeCategory(LoginRequiredMixin, View):
    def get(self, request, incomecat_id=None):
        if incomecat_id:
            income_category = models.IncomeCategory.objects.get(pk=incomecat_id)
            income_category_form = forms.IncomeCategoryForm(instance=income_category)
        else:
            income_category_form = forms.IncomeCategoryForm()
        return render(request,
                      'incomeCategories/create.html',
                      {'form': income_category_form})

    def post(self, request, incomecat_id=None):
        if not incomecat_id:
            income_category_form = forms.IncomeCategoryForm(request.POST, files=request.FILES)
            if income_category_form.is_valid():
                new_category = income_category_form.save(commit=False)
                new_category.user = request.user
                new_category.slug = slugify(new_category.name)
                new_category.save()
                if new_category.image:
                    edit_image(new_category.image.path)
                return render(request,
                              'incomeCategories/incomecategory_detail.html',
                              {'category': new_category})
        else:
            income_category = models.IncomeCategory.objects.get(pk=incomecat_id)
            income_category_form = forms.IncomeCategoryForm(request.POST, instance=income_category, files=request.FILES)
            if income_category_form.is_valid():
                new_category = income_category_form.save(commit=False)
                new_category.user = request.user
                new_category.slug = slugify(new_category.name)
                new_category.save()
                if new_category.image:
                    edit_image(new_category.image.path)
                return redirect(new_category)


class Cost(LoginRequiredMixin, View):
    def get(self, request, cost_id=None):
        if cost_id:
            cost = models.Cost.objects.get(pk=cost_id)
            cost_form = forms.CostForm(instance=cost, user=request.user)
        else:
            cost_form = forms.CostForm(user=request.user)
        return render(request,
                      'costs/create.html',
                      {'form': cost_form})

    def post(self, request, cost_id=None):
        if not cost_id:
            cost_form = forms.CostForm(request.user, request.POST)
            if cost_form.is_valid():
                new_cost = cost_form.save(commit=False)
                new_cost.user = request.user
                new_cost.account.balance -= rates.get_byn(new_cost.value, new_cost.currency)
                new_cost.save()
                new_cost.account.save()
        else:
            cost = models.Cost.objects.get(pk=cost_id)
            old_value = cost.value
            old_currency = cost.currency
            old_account = cost.account
            cost_form = forms.CostForm(request.user, request.POST, instance=cost)
            if cost_form.is_valid():
                new_cost = cost_form.save(commit=False)
                new_cost.user = request.user
                if old_account == new_cost.account:
                    new_cost.account.balance += rates.get_byn(old_value, old_currency)
                    if old_account:
                        old_account.save()
                else:
                    if old_account:
                        old_account.balance += rates.get_byn(old_value, old_currency)
                        old_account.save()
                new_cost.account.balance -= rates.get_byn(new_cost.value, new_cost.currency)
                new_cost.save()
                new_cost.account.save()
        return redirect(new_cost.category,
                            user_id=new_cost.user.pk,
                            slug=new_cost.category.slug)


@login_required
def cost_delete(request, cost_id):
    cost = get_object_or_404(models.Cost, id=cost_id)

    if request.method == "POST":
        cost.account.balance += rates.get_byn(cost.value, cost.currency)
        cost.account.save()
        cost.delete()
        return redirect("wallet:costcategory_details",
                        user_id=request.user.id,
                        slug=cost.category.slug)
    else:
        return render(request,
                      'delete.html',
                      {'obj_type': 'cost',
                       'object': cost})


class Income(LoginRequiredMixin, View):
    def get(self, request, income_id=None):
        if income_id:
            income = models.Income.objects.get(pk=income_id)
            income_form = forms.IncomeForm(instance=income, user=request.user)
        else:
            income_form = forms.IncomeForm(user=request.user)
        return render(request,
                      'incomes/create.html',
                      {'form': income_form})

    def post(self, request, income_id=None):
        if not income_id:
            income_form = forms.IncomeForm(request.user, request.POST)
            if income_form.is_valid():
                new_income = income_form.save(commit=False)
                new_income.user = request.user
                new_income.account.balance += rates.get_byn(new_income.value, new_income.currency)
                new_income.save()
                new_income.account.save()
        else:
            income = models.Income.objects.get(pk=income_id)
            old_value = income.value
            old_currency = income.currency
            old_account = income.account
            income_form = forms.IncomeForm(request.user, request.POST, instance=income)
            if income_form.is_valid():
                new_income = income_form.save(commit=False)
                new_income.user = request.user
                if old_account == new_income.account:
                    new_income.account.balance -= rates.get_byn(old_value, old_currency)
                    if old_account:
                        old_account.save()
                else:
                    if old_account:
                        old_account.balance -= rates.get_byn(old_value, old_currency)
                        old_account.save()
                new_income.account.balance += rates.get_byn(new_income.value, new_income.currency)
                new_income.save()
                new_income.account.save()
        return redirect(new_income.category,
                            user_id=new_income.user.pk,
                            slug=new_income.category.slug)


@login_required
def income_delete(request, income_id):
    income = get_object_or_404(models.Income, id=income_id)

    if request.method == "POST":
        if income.account:
            income.account.balance -= rates.get_byn(income.value, income.currency)
            income.account.save()
        income.delete()
        return redirect("wallet:incomecategory_details",
                        user_id=request.user.id,
                        slug=income.category.slug)
    else:
        return render(request,
                      'delete.html',
                      {'obj_type': 'income',
                       'object': income})


class TransferCreate(LoginRequiredMixin, View):
    def get(self, request):
        transfer_form = forms.TransferForm(user=request.user)
        return render(request,
                      'transfers/create.html',
                      {'form': transfer_form})

    def post(self, request):
        transfer_form = forms.TransferForm(request.user, request.POST)
        if transfer_form.is_valid():
            new_transfer = transfer_form.save(commit=False)
            new_transfer.user = request.user
            new_transfer.from_account.balance -= new_transfer.value_from
            new_transfer.to_account.balance += new_transfer.value_from
            new_transfer.from_account.save()
            new_transfer.to_account.save()
            new_transfer.save()
            return redirect('wallet:all_accounts')


def register(request):
    if request.method == "POST":
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'],
            )
            new_user.save()
            for cat, img_src in zip(DEFAULT_COST_CATEGORIES, DEFAULT_COST_ICONS):
                models.CostCategory.objects.create(
                    name=cat,
                    user=new_user,
                    slug=slugify(cat),
                    image=img_src
                )
            for cat, img_src in zip(DEFAULT_INCOME_CATEGORIES, DEFAULT_INCOME_ICONS):
                models.IncomeCategory.objects.create(
                    name=cat,
                    user=new_user,
                    slug=slugify(cat),
                    image=img_src
                )
            for acc, img_src in zip(DEFAULT_ACCOUNTS, DEFAULT_ACCOUNTS_ICONS):
                new_acc = models.Account(
                    name=acc,
                    balance=0,
                    user=new_user,
                    slug=slugify(acc),
                    image=img_src
                )
                new_acc.save()
            return render(request, 'registration/registration_complete.html',
                          {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request, 'registration/registration.html', {'form': user_form})


def edit_image(src):
    im = Image.open(src)
    ratio = max(im.size) / ICON_SIZE
    new_size = (round(size / ratio) for size in im.size)
    im = im.resize(new_size)
    im.save(src, quality=100)
