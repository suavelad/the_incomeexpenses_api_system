from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
 
router = DefaultRouter()


router.register('income',views.IncomeViewSet, 'user')

urlpatterns = router.urls

urlpatterns += [
    # path('', views.IncomeListAPIView.as_view(), name="incomes"),
    # path('<int:id>', views.IncomeDetailAPIView.as_view(), name="income"),
]