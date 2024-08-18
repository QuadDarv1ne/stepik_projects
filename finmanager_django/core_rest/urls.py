# core_rest/urls.py

from django.urls import path
from .views import register_user, login_user, user_list, transaction_list, budget_list

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('users/', user_list, name='user_list'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('budgets/', budget_list, name='budget_list'),
]
