from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

PO_STATUS = [
    ('draft', _('Draft')),
    ('sent', _('Sent')),
    ('confirmed', _('Confirmed')),
    ('received', _('Received')),
    ('cancelled', _('Cancelled')),
]

class Supplier(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=50, blank=True, verbose_name=_('Phone'))
    address = models.TextField(blank=True, verbose_name=_('Address'))
    tax_id = models.CharField(max_length=50, blank=True, verbose_name=_('Tax Id'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'purchase_orders_supplier'

    def __str__(self):
        return self.name


class PurchaseOrder(HubBaseModel):
    order_number = models.CharField(max_length=50, unique=True, verbose_name=_('Order Number'))
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, default='draft', choices=PO_STATUS, verbose_name=_('Status'))
    order_date = models.DateField(auto_now_add=True, verbose_name=_('Order Date'))
    expected_date = models.DateField(null=True, blank=True, verbose_name=_('Expected Date'))
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Subtotal'))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Tax Amount'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Total'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'purchase_orders_purchaseorder'

    def __str__(self):
        return str(self.id)


class PurchaseOrderLine(HubBaseModel):
    order = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE, related_name='lines')
    description = models.CharField(max_length=255, verbose_name=_('Description'))
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default='1', verbose_name=_('Quantity'))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Unit Price'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Total'))

    class Meta(HubBaseModel.Meta):
        db_table = 'purchase_orders_purchaseorderline'

    def __str__(self):
        return str(self.id)

