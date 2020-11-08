from django.urls import path

from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.AllCostCategories.as_view(), name='all_cost_categories'),
    path('incomecategory/', views.AllIncomeCategories.as_view(), name='all_income_categories'),
    path('accounts/', views.AllAccounts.as_view(), name='all_accounts'),
    path('<int:user_id>/costcategory/<slug:slug>/',
         views.CostCategory.as_view(),
         name='costcategory_details'),
    path('<int:user_id>/incomecategory/<slug:slug>/',
         views.IncomeCategory.as_view(),
         name='incomecategory_details'),
    path('<int:user_id>/account/<slug:slug>/',
         views.AccountDetail.as_view(),
         name='account_details'),
    path('costcategory/create/', views.CreateCostCategory.as_view(), name='costcategory_create'),
    path('incomecategory/create/', views.CreateIncomeCategory.as_view(), name='incomecategory_create'),
    path('cost/create/', views.Cost.as_view(), name='cost_create'),
    path('income/create/', views.Income.as_view(), name='income_create'),
    path('account/create/', views.Account.as_view(), name='account_create'),
    path('cost/<int:cost_id>/', views.Cost.as_view(), name='cost_edit'),
    ]
