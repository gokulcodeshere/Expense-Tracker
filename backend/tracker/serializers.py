from rest_framework import serializers
from .models import UserProfile, Category, Transaction, SavingGoal

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SavingGoalSerializer(serializers.ModelSerializer):
    remaining_amount = serializers.SerializerMethodField()

    class Meta:
        model = SavingGoal
        fields = '__all__'

    def get_remaining_amount(self, obj):
        return obj.remaining_amount()