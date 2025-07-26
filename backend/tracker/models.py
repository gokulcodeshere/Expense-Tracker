from django.db import models
from django.contrib.auth.models import User

# UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    minimum_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    enable_minimum_balance = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_expense = models.BooleanField(default=True)  # True = Expense, False = Income

    def __str__(self):
        return f"{self.name} ({'Expense' if self.is_expense else 'Income'})"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_expense = models.BooleanField(default=True)  # True = Expense, False = Income
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        type_str = "Expense" if self.is_expense else "Income"
        return f"{self.title} - {type_str} - ₹{self.amount} on {self.date}"

class SavingGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    deadline = models.DateField()

    def __str__(self):
        return self.title
    
    def remaining_amount(self):
        return max(0, self.goal_amount - self.current_balance)
