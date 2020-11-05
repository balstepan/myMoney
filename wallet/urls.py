from django.urls import path

from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.AllCostCategories.as_view(), name='all_cost_categories'),
    path('<int:user_id>/costcategory/<slug:slug>/',
         views.CostCategory.as_view(),
         name='costcategory_details'),
    path('costcategory/create/', views.CreateCostCategory.as_view(), name='costcategory_create'),
    ]
