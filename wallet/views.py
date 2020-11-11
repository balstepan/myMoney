from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from pytils.translit import slugify

from . import models
from . import forms


class AllAccounts(View):
    def get(self, request):
        accounts = models.Account.objects.filter(user=request.user)
        return render(request,
                      'accounts/all_accounts.html',
                      {'accounts': accounts})


class AccountDetail(View):
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
            account_form = forms.AccountForm(request.POST, instance=account)
        else:
            account_form = forms.AccountForm(request.POST)
        if account_form.is_valid():
            new_account = account_form.save(commit=False)
            new_account.user = request.user
            new_account.slug = slugify(new_account.name)
            new_account.save()
        return redirect('wallet:all_accounts')


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


class AllCostCategories(View):

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
                costs = cat_for_count.costs.filter(created_at__gt=datetime.now()-timedelta(days=days))
                amount += sum(cost.value for cost in costs)
            amounts.append(amount)
        context = zip(cost_categories_list, amounts)
        return render(request,
                      'costCategories/all_categories.html',
                      {'categories': context})


class CostCategory(View):

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


class CreateCostCategory(View):
    def get(self, request, costcat_id=None):
        if costcat_id:
            cost_category = models.CostCategory.objects.get(pk=costcat_id)
            cost_category_form = forms.CostCategoryForm(instance=cost_category)
        else:
            cost_category_form = forms.CostCategoryForm()
        return render(request,
                      'costCategories/create.html',
                      {'form': cost_category_form})

    def post(self, request, costcat_id=None):
        if not costcat_id:
            cost_category_form = forms.CostCategoryForm(request.POST)
            if cost_category_form.is_valid():
                new_category = cost_category_form.save(commit=False)
                new_category.user = request.user
                new_category.slug = slugify(new_category.name)
                new_category.color = 'green'
                new_category.save()
                return render(request,
                          'costCategories/costcategory_detail.html',
                          {'category': new_category})
        else:
            cost_category = models.CostCategory.objects.get(pk=costcat_id)
            cost_category_form = forms.CostCategoryForm(request.POST, instance=cost_category)
            if cost_category_form.is_valid():
                new_category = cost_category_form.save(commit=False)
                new_category.user = request.user
                new_category.slug = slugify(new_category.name)
                new_category.save()
                return redirect(new_category)


class AllIncomeCategories(View):

    def get(self, request, days=30):
        income_categories_list = models.IncomeCategory.objects.filter(user=request.user)
        amounts = []
        for cat in income_categories_list:
            incomes = cat.incomes.filter(created_at__gt=datetime.now()-timedelta(days=days))
            amount = sum(income.value for income in incomes)
            amounts.append(amount)
        context = zip(income_categories_list, amounts)
        return render(request,
                      'incomeCategories/all_categories.html',
                      {'categories': context})


class IncomeCategory(View):

    def get(self, request, user_id, slug, days=30):
        category = get_object_or_404(models.IncomeCategory, slug=slug,
                                     user=get_object_or_404(models.User, pk=user_id))
        incomes = category.incomes.filter(created_at__gt=datetime.now()-timedelta(days=days)).order_by('-created_at')
        return render(request,
                      'incomeCategories/incomecategory_detail.html',
                      {'category': category,
                       'incomes': incomes})


class CreateIncomeCategory(View):
    def get(self, request):
        income_category_form = forms.IncomeCategoryForm()
        return render(request,
                      'incomeCategories/create.html',
                      {'form': income_category_form})

    def post(self, request):
        income_category_form = forms.IncomeCategoryForm(request.POST)
        if income_category_form.is_valid():
            new_category = income_category_form.save(commit=False)
            new_category.user = request.user
            new_category.slug = slugify(new_category.name)
            new_category.color = 'green'
            new_category.save()
            return render(request,
                          'incomeCategories/incomecategory_detail.html',
                          {'category': new_category})


class Cost(View):
    def get(self, request, cost_id=None):
        if cost_id:
            cost = models.Cost.objects.get(pk=cost_id)
            cost_form = forms.CostForm(instance=cost)
        else:
            cost_form = forms.CostForm()
        return render(request,
                      'costs/create.html',
                      {'form': cost_form})

    def post(self, request, cost_id=None):
        if not cost_id:
            cost_form = forms.CostForm(request.POST)
            if cost_form.is_valid():
                new_cost = cost_form.save(commit=False)
                new_cost.user = request.user
                new_cost.account.balance -= new_cost.value
                new_cost.save()
                new_cost.account.save()
        else:
            cost = models.Cost.objects.get(pk=cost_id)
            old_value = cost.value
            old_account = cost.account
            cost_form = forms.CostForm(request.POST, instance=cost)
            if cost_form.is_valid():
                new_cost = cost_form.save(commit=False)
                new_cost.user = request.user
                if old_account == new_cost.account:
                    new_cost.account.balance += old_value
                    if old_account:
                        old_account.save()
                else:
                    if old_account:
                        old_account.balance += old_value
                        old_account.save()
                new_cost.account.balance -= new_cost.value
                new_cost.save()
                new_cost.account.save()
        return redirect(new_cost.category,
                            user_id=new_cost.user.pk,
                            slug=new_cost.category.slug)


def cost_delete(request, cost_id):
    cost = get_object_or_404(models.Cost, id=cost_id)

    if request.method == "POST":
        cost.account.balance += cost.value
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


class Income(View):
    def get(self, request, income_id=None):
        if income_id:
            income = models.Income.objects.get(pk=income_id)
            income_form = forms.IncomeForm(instance=income)
        else:
            income_form = forms.IncomeForm()
        return render(request,
                      'incomes/create.html',
                      {'form': income_form})

    def post(self, request, income_id=None):
        if not income_id:
            income_form = forms.IncomeForm(request.POST)
            if income_form.is_valid():
                new_income = income_form.save(commit=False)
                new_income.user = request.user
                new_income.account.balance += new_income.value
                new_income.save()
                new_income.account.save()
        else:
            income = models.Income.objects.get(pk=income_id)
            old_value = income.value
            old_account = income.account
            income_form = forms.IncomeForm(request.POST, instance=income)
            if income_form.is_valid():
                new_income = income_form.save(commit=False)
                new_income.user = request.user
                if old_account == new_income.account:
                    new_income.account.balance -= old_value
                    if old_account:
                        old_account.save()
                else:
                    if old_account:
                        old_account.balance -= old_value
                        old_account.save()
                new_income.account.balance += new_income.value
                new_income.save()
                new_income.account.save()
        return redirect(new_income.category,
                            user_id=new_income.user.pk,
                            slug=new_income.category.slug)


def income_delete(request, income_id):
    income = get_object_or_404(models.Income, id=income_id)

    if request.method == "POST":
        income.account.balance -= income.value
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
