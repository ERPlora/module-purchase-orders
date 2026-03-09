# Purchase Orders

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `purchase_orders` |
| **Version** | `1.0.0` |
| **Icon** | `bag-handle-outline` |
| **Dependencies** | None |

## Models

### `Supplier`

Supplier(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, email, phone, address, tax_id, notes, is_active)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `email` | EmailField | max_length=254, optional |
| `phone` | CharField | max_length=50, optional |
| `address` | TextField | optional |
| `tax_id` | CharField | max_length=50, optional |
| `notes` | TextField | optional |
| `is_active` | BooleanField |  |

### `PurchaseOrder`

PurchaseOrder(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, order_number, supplier, status, order_date, expected_date, subtotal, tax_amount, total, notes)

| Field | Type | Details |
|-------|------|---------|
| `order_number` | CharField | max_length=50 |
| `supplier` | ForeignKey | → `purchase_orders.Supplier`, on_delete=CASCADE |
| `status` | CharField | max_length=20, choices: draft, sent, confirmed, received, cancelled |
| `order_date` | DateField | optional |
| `expected_date` | DateField | optional |
| `subtotal` | DecimalField |  |
| `tax_amount` | DecimalField |  |
| `total` | DecimalField |  |
| `notes` | TextField | optional |

### `PurchaseOrderLine`

PurchaseOrderLine(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, order, description, quantity, unit_price, total)

| Field | Type | Details |
|-------|------|---------|
| `order` | ForeignKey | → `purchase_orders.PurchaseOrder`, on_delete=CASCADE |
| `description` | CharField | max_length=255 |
| `quantity` | DecimalField |  |
| `unit_price` | DecimalField |  |
| `total` | DecimalField |  |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `PurchaseOrder` | `supplier` | `purchase_orders.Supplier` | CASCADE | No |
| `PurchaseOrderLine` | `order` | `purchase_orders.PurchaseOrder` | CASCADE | No |

## URL Endpoints

Base path: `/m/purchase_orders/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `orders/` | `orders` | GET |
| `suppliers/` | `suppliers_list` | GET |
| `suppliers/add/` | `supplier_add` | GET/POST |
| `suppliers/<uuid:pk>/edit/` | `supplier_edit` | GET |
| `suppliers/<uuid:pk>/delete/` | `supplier_delete` | GET/POST |
| `suppliers/<uuid:pk>/toggle/` | `supplier_toggle_status` | GET |
| `suppliers/bulk/` | `suppliers_bulk_action` | GET/POST |
| `purchase_order_lines/` | `purchase_order_lines_list` | GET |
| `purchase_order_lines/add/` | `purchase_order_line_add` | GET/POST |
| `purchase_order_lines/<uuid:pk>/edit/` | `purchase_order_line_edit` | GET |
| `purchase_order_lines/<uuid:pk>/delete/` | `purchase_order_line_delete` | GET/POST |
| `purchase_order_lines/bulk/` | `purchase_order_lines_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `purchase_orders.view_purchaseorder` | View Purchaseorder |
| `purchase_orders.add_purchaseorder` | Add Purchaseorder |
| `purchase_orders.change_purchaseorder` | Change Purchaseorder |
| `purchase_orders.delete_purchaseorder` | Delete Purchaseorder |
| `purchase_orders.view_supplier` | View Supplier |
| `purchase_orders.add_supplier` | Add Supplier |
| `purchase_orders.change_supplier` | Change Supplier |
| `purchase_orders.delete_supplier` | Delete Supplier |
| `purchase_orders.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_purchaseorder`, `add_supplier`, `change_purchaseorder`, `change_supplier`, `view_purchaseorder`, `view_supplier`
- **employee**: `add_purchaseorder`, `view_purchaseorder`, `view_supplier`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Orders | `bag-handle-outline` | `orders` | No |
| Suppliers | `business-outline` | `suppliers` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_purchase_orders`

List purchase orders with optional filters.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter: draft, sent, confirmed, received, cancelled |
| `supplier_id` | string | No | Filter by supplier ID |
| `limit` | integer | No | Max results (default 20) |

### `create_purchase_order`

Create a new purchase order for a supplier.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `supplier_id` | string | Yes | Supplier ID |
| `notes` | string | No | Order notes |
| `expected_date` | string | No | Expected delivery date (YYYY-MM-DD) |
| `lines` | array | No | Order lines |

### `list_suppliers`

List suppliers.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `search` | string | No | Search by name |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  purchase_orders/
    css/
    js/
templates/
  purchase_orders/
    pages/
      dashboard.html
      index.html
      orders.html
      purchase_order_line_add.html
      purchase_order_line_edit.html
      purchase_order_lines.html
      settings.html
      supplier_add.html
      supplier_edit.html
      suppliers.html
    partials/
      dashboard_content.html
      orders_content.html
      panel_purchase_order_line_add.html
      panel_purchase_order_line_edit.html
      panel_supplier_add.html
      panel_supplier_edit.html
      purchase_order_line_add_content.html
      purchase_order_line_edit_content.html
      purchase_order_lines_content.html
      purchase_order_lines_list.html
      settings_content.html
      supplier_add_content.html
      supplier_edit_content.html
      suppliers_content.html
      suppliers_list.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
