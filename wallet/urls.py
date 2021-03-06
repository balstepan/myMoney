from django.urls import path


from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('costcategories/', views.AllCostCategories.as_view(), name='all_cost_categories'),
    path('incomecategories/', views.AllIncomeCategories.as_view(), name='all_income_categories'),
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
    path('account/create/', views.AccountDetail.as_view(), name='account_create'),
    path('cost/<int:cost_id>/', views.Cost.as_view(), name='cost_edit'),
    path('income/<int:income_id>/', views.Income.as_view(), name='income_edit'),
    path('costcategory/<int:costcat_id>/', views.CreateCostCategory.as_view(), name='costcategory_edit'),
    path('incomecategory/<int:incomecat_id>/', views.CreateIncomeCategory.as_view(), name='incomecategory_edit'),
    path('account/delete/<int:acc_id>/', views.account_delete, name='account_delete'),
    path('cost/delete/<int:cost_id>/', views.cost_delete, name='cost_delete'),
    path('income/delete/<int:income_id>/', views.income_delete, name='income_delete'),
    path('costcategory/delete/<int:costcat_id>/', views.cost_category_delete, name='costcategory_delete'),
    path('incomecategory/delete/<int:incomecat_id>/', views.income_category_delete, name='incomecategory_delete'),
    path('transfer/create/', views.TransferCreate.as_view(), name='transfer_create'),
    path('register/', views.register, name='register'),
    path('access-denied/', views.access_denied, name='access_denied'),
    ]
