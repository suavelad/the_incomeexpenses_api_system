from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
 
router = DefaultRouter()


router.register('expenses',views.ExpenseViewSet, 'user')

urlpatterns = router.urls
urlpatterns += [
    # path('', views.ExpenseListAPIView.as_view(), name="expenses"),
    # path('<int:id>', views.ExpenseDetailAPIView.as_view(), name="expense"),
]