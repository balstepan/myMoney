from django.urls import path
from django.contrib.auth import views as auth_views
# from django.contrib.authentication.urls

app_name = 'authentication'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]
