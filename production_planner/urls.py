from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductionBatchListView, ProductionBatchViewSet

app_name = 'production_planner'

router = DefaultRouter()
router.register(r'batches', ProductionBatchViewSet, basename='batch')

urlpatterns = [
    path('batches-list/', ProductionBatchListView.as_view(), name='batch-list'),
    path('api/', include(router.urls)),
]