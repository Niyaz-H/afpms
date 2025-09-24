from django.urls import path
from .views import HomeView, FactoryManagerDashboardView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', FactoryManagerDashboardView.as_view(), name='dashboard'),
]