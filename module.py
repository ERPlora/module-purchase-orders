from django.utils.translation import gettext_lazy as _

MODULE_ID = 'purchase_orders'
MODULE_NAME = _('Purchase Orders')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'bag-handle-outline'
MODULE_DESCRIPTION = _('Purchase orders and supplier management')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'commerce'

MENU = {
    'label': _('Purchase Orders'),
    'icon': 'bag-handle-outline',
    'order': 15,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Orders'), 'icon': 'bag-handle-outline', 'id': 'orders'},
{'label': _('Suppliers'), 'icon': 'business-outline', 'id': 'suppliers'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'purchase_orders.view_purchaseorder',
'purchase_orders.add_purchaseorder',
'purchase_orders.change_purchaseorder',
'purchase_orders.delete_purchaseorder',
'purchase_orders.view_supplier',
'purchase_orders.add_supplier',
'purchase_orders.change_supplier',
'purchase_orders.delete_supplier',
'purchase_orders.manage_settings',
]
