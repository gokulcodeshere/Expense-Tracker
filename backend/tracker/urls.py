from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'saving-goals', SavingGoalViewSet)
router.register(r'user-profiles', UserProfileViewSet)

urlpatterns = router.urls
