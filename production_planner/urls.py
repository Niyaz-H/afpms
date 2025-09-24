from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductionBatchListView,
    ProductionBatchViewSet,
    DemandForecastView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView
)

app_name = 'production_planner'

router = DefaultRouter()
router.register(r'batches', ProductionBatchViewSet, basename='batch')

urlpatterns = [
    path('batches-list/', ProductionBatchListView.as_view(), name='batch-list'),
    path('demand-forecast/', DemandForecastView.as_view(), name='demand-forecast'),
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('api/', include(router.urls)),
]