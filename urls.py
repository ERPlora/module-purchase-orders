from django.urls import path
from . import views

app_name = 'purchase_orders'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('orders/', views.purchase_order_lines_list, name='orders'),


    # Supplier
    path('suppliers/', views.suppliers_list, name='suppliers_list'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),
    path('suppliers/<uuid:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    path('suppliers/<uuid:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    path('suppliers/<uuid:pk>/toggle/', views.supplier_toggle_status, name='supplier_toggle_status'),
    path('suppliers/bulk/', views.suppliers_bulk_action, name='suppliers_bulk_action'),

    # PurchaseOrderLine
    path('purchase_order_lines/', views.purchase_order_lines_list, name='purchase_order_lines_list'),
    path('purchase_order_lines/add/', views.purchase_order_line_add, name='purchase_order_line_add'),
    path('purchase_order_lines/<uuid:pk>/edit/', views.purchase_order_line_edit, name='purchase_order_line_edit'),
    path('purchase_order_lines/<uuid:pk>/delete/', views.purchase_order_line_delete, name='purchase_order_line_delete'),
    path('purchase_order_lines/bulk/', views.purchase_order_lines_bulk_action, name='purchase_order_lines_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
