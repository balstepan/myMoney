from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
from django.views import View

from . import models


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

    def get(self, request, slug, days=30):
        category = get_object_or_404(models.CostCategory, slug=slug)
        children = category.children.all()
        costs = category.costs.filter(created_at__gt=datetime.now()-timedelta(days=days))
        return render(request,
                      'costCategories/costcategory_detail.html',
                      {'category': category,
                       'children': children,
                       'costs': costs})
