"""
Purchase Orders Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import Supplier, PurchaseOrder, PurchaseOrderLine

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('purchase_orders', 'dashboard')
@htmx_view('purchase_orders/pages/index.html', 'purchase_orders/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_suppliers': Supplier.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_purchase_order_lines': PurchaseOrderLine.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# Supplier
# ======================================================================

SUPPLIER_SORT_FIELDS = {
    'name': 'name',
    'is_active': 'is_active',
    'email': 'email',
    'phone': 'phone',
    'address': 'address',
    'tax_id': 'tax_id',
    'created_at': 'created_at',
}

def _build_suppliers_context(hub_id, per_page=10):
    qs = Supplier.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'suppliers': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_suppliers_list(request, hub_id, per_page=10):
    ctx = _build_suppliers_context(hub_id, per_page)
    return django_render(request, 'purchase_orders/partials/suppliers_list.html', ctx)

@login_required
@with_module_nav('purchase_orders', 'suppliers')
@htmx_view('purchase_orders/pages/suppliers.html', 'purchase_orders/partials/suppliers_content.html')
def suppliers_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Supplier.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query) | Q(phone__icontains=search_query) | Q(address__icontains=search_query))

    order_by = SUPPLIER_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'is_active', 'email', 'phone', 'address', 'tax_id']
        headers = ['Name', 'Is Active', 'Email', 'Phone', 'Address', 'Tax Id']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='suppliers.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='suppliers.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'purchase_orders/partials/suppliers_list.html', {
            'suppliers': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'suppliers': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
@htmx_view('purchase_orders/pages/supplier_add.html', 'purchase_orders/partials/supplier_add_content.html')
def supplier_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        tax_id = request.POST.get('tax_id', '').strip()
        notes = request.POST.get('notes', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        obj = Supplier(hub_id=hub_id)
        obj.name = name
        obj.email = email
        obj.phone = phone
        obj.address = address
        obj.tax_id = tax_id
        obj.notes = notes
        obj.is_active = is_active
        obj.save()
        response = HttpResponse(status=204)
        response['HX-Redirect'] = reverse('purchase_orders:suppliers_list')
        return response
    return {}

@login_required
@htmx_view('purchase_orders/pages/supplier_edit.html', 'purchase_orders/partials/supplier_edit_content.html')
def supplier_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Supplier, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.email = request.POST.get('email', '').strip()
        obj.phone = request.POST.get('phone', '').strip()
        obj.address = request.POST.get('address', '').strip()
        obj.tax_id = request.POST.get('tax_id', '').strip()
        obj.notes = request.POST.get('notes', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_suppliers_list(request, hub_id)
    return {'obj': obj}

@login_required
@require_POST
def supplier_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Supplier, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_suppliers_list(request, hub_id)

@login_required
@require_POST
def supplier_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Supplier, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_suppliers_list(request, hub_id)

@login_required
@require_POST
def suppliers_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Supplier.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_suppliers_list(request, hub_id)


# ======================================================================
# PurchaseOrderLine
# ======================================================================

PURCHASE_ORDER_LINE_SORT_FIELDS = {
    'order': 'order',
    'total': 'total',
    'unit_price': 'unit_price',
    'quantity': 'quantity',
    'description': 'description',
    'created_at': 'created_at',
}

def _build_purchase_order_lines_context(hub_id, per_page=10):
    qs = PurchaseOrderLine.objects.filter(hub_id=hub_id, is_deleted=False).order_by('order')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'purchase_order_lines': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'order',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_purchase_order_lines_list(request, hub_id, per_page=10):
    ctx = _build_purchase_order_lines_context(hub_id, per_page)
    return django_render(request, 'purchase_orders/partials/purchase_order_lines_list.html', ctx)

@login_required
@with_module_nav('purchase_orders', 'orders')
@htmx_view('purchase_orders/pages/purchase_order_lines.html', 'purchase_orders/partials/purchase_order_lines_content.html')
def purchase_order_lines_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'order')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = PurchaseOrderLine.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(description__icontains=search_query))

    order_by = PURCHASE_ORDER_LINE_SORT_FIELDS.get(sort_field, 'order')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['order', 'total', 'unit_price', 'quantity', 'description']
        headers = ['PurchaseOrder', 'Total', 'Unit Price', 'Quantity', 'Description']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='purchase_order_lines.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='purchase_order_lines.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'purchase_orders/partials/purchase_order_lines_list.html', {
            'purchase_order_lines': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'purchase_order_lines': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
@htmx_view('purchase_orders/pages/purchase_order_line_add.html', 'purchase_orders/partials/purchase_order_line_add_content.html')
def purchase_order_line_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        quantity = request.POST.get('quantity', '0') or '0'
        unit_price = request.POST.get('unit_price', '0') or '0'
        total = request.POST.get('total', '0') or '0'
        obj = PurchaseOrderLine(hub_id=hub_id)
        obj.description = description
        obj.quantity = quantity
        obj.unit_price = unit_price
        obj.total = total
        obj.save()
        response = HttpResponse(status=204)
        response['HX-Redirect'] = reverse('purchase_orders:purchase_order_lines_list')
        return response
    return {}

@login_required
@htmx_view('purchase_orders/pages/purchase_order_line_edit.html', 'purchase_orders/partials/purchase_order_line_edit_content.html')
def purchase_order_line_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(PurchaseOrderLine, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.description = request.POST.get('description', '').strip()
        obj.quantity = request.POST.get('quantity', '0') or '0'
        obj.unit_price = request.POST.get('unit_price', '0') or '0'
        obj.total = request.POST.get('total', '0') or '0'
        obj.save()
        return _render_purchase_order_lines_list(request, hub_id)
    return {'obj': obj}

@login_required
@require_POST
def purchase_order_line_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(PurchaseOrderLine, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_purchase_order_lines_list(request, hub_id)

@login_required
@require_POST
def purchase_order_lines_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = PurchaseOrderLine.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_purchase_order_lines_list(request, hub_id)


@login_required
@permission_required('purchase_orders.manage_settings')
@with_module_nav('purchase_orders', 'settings')
@htmx_view('purchase_orders/pages/settings.html', 'purchase_orders/partials/settings_content.html')
def settings_view(request):
    return {}

