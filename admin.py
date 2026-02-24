from django.contrib import admin

from .models import Supplier, PurchaseOrder, PurchaseOrderLine

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'tax_id', 'created_at']
    search_fields = ['name', 'email', 'phone', 'address']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'supplier', 'status', 'expected_date', 'subtotal', 'created_at']
    search_fields = ['order_number', 'status', 'notes']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PurchaseOrderLine)
class PurchaseOrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'description', 'quantity', 'unit_price', 'total', 'created_at']
    search_fields = ['description']
    readonly_fields = ['created_at', 'updated_at']

