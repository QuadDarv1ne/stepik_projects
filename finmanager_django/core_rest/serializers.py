# core_rest/serializers.py

from rest_framework import serializers
from core.models import CustomUser
from .models import Transaction, Budget

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'is_active', 'is_staff']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'description', 'date']

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['user', 'category', 'amount', 'start_date', 'end_date']
