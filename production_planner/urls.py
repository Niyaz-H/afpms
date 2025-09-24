from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductionBatchListView, ProductionBatchViewSet, DemandForecastView

app_name = 'production_planner'

router = DefaultRouter()
router.register(r'batches', ProductionBatchViewSet, basename='batch')

urlpatterns = [
    path('batches-list/', ProductionBatchListView.as_view(), name='batch-list'),
    path('demand-forecast/', DemandForecastView.as_view(), name='demand-forecast'),
    path('api/', include(router.urls)),
]