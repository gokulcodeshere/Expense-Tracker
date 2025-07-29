from django.contrib import admin
from .models import UserProfile, Category, Transaction, SavingGoal

admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(SavingGoal)
admin.site.register(Category)

# Register your models here.
