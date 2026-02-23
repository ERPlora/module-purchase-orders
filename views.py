"""
Purchase Orders Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('purchase_orders', 'dashboard')
@htmx_view('purchase_orders/pages/dashboard.html', 'purchase_orders/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('purchase_orders', 'orders')
@htmx_view('purchase_orders/pages/orders.html', 'purchase_orders/partials/orders_content.html')
def orders(request):
    """Orders view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('purchase_orders', 'suppliers')
@htmx_view('purchase_orders/pages/suppliers.html', 'purchase_orders/partials/suppliers_content.html')
def suppliers(request):
    """Suppliers view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('purchase_orders', 'settings')
@htmx_view('purchase_orders/pages/settings.html', 'purchase_orders/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

