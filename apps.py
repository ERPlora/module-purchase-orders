from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PurchaseOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchase_orders'
    label = 'purchase_orders'
    verbose_name = _('Purchase Orders')

    def ready(self):
        pass
