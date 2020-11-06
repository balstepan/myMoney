from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from pytils.translit import slugify

from . import models
from . import forms


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
    def get(self, request):
        cost_category_form = forms.CostCategoryForm()
        return render(request,
                      'costCategories/create.html',
                      {'form': cost_category_form})

    def post(self, request):
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


class Cost(View):
    def get(self, request):
        cost_form = forms.CostForm()
        return render(request,
                      'costs/create.html',
                      {'form': cost_form})

    def post(self, request):
        cost_form = forms.CostForm(request.POST)
        if cost_form.is_valid():
            new_cost = cost_form.save(commit=False)
            new_cost.user = request.user
            new_cost.account.balance -= new_cost.value
            new_cost.save()
            new_cost.account.save()
            return redirect(new_cost.category,
                            user_id=new_cost.user.pk,
                            slug=new_cost.category.slug)
