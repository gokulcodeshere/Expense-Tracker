from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, SavingGoal, Category, UserProfile
from .serializers import (
    TransactionSerializer,
    SavingGoalSerializer,
    CategorySerializer,
    UserProfileSerializer,
)


from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary data for dashboard"""
        user = request.user
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        # Get current month transactions
        current_month_transactions = Transaction.objects.filter(
            user=user,
            date__year=current_year,
            date__month=current_month
        )
        
        # Calculate totals
        total_income = current_month_transactions.filter(
            is_expense=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_expenses = current_month_transactions.filter(
            is_expense=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        net_savings = total_income - total_expenses
        
        # Get monthly data for the last 6 months
        monthly_data = []
        for i in range(6):
            month_date = timezone.now() - timedelta(days=30*i)
            month_transactions = Transaction.objects.filter(
                user=user,
                date__year=month_date.year,
                date__month=month_date.month
            )
            
            month_income = month_transactions.filter(
                is_expense=False
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            month_expenses = month_transactions.filter(
                is_expense=True
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            monthly_data.append({
                'month': month_date.strftime('%B %Y'),
                'income': month_income,
                'expenses': month_expenses
            })
        
        # Get category-wise expense breakdown
        category_expenses = current_month_transactions.filter(
            is_expense=True
        ).values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        return Response({
            'summary': {
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net_savings': net_savings
            },
            'monthly_data': monthly_data,
            'category_expenses': list(category_expenses)
        })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavingGoalViewSet(viewsets.ModelViewSet):
    queryset = SavingGoal.objects.all()
    serializer_class = SavingGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavingGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
