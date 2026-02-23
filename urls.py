from django.urls import path
from . import views

app_name = 'purchase_orders'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.orders, name='orders'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('settings/', views.settings, name='settings'),
]
