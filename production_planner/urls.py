from django.urls import path
from .views import ProductionBatchListView

app_name = 'production_planner'

urlpatterns = [
    path('batches/', ProductionBatchListView.as_view(), name='batch-list'),
]