# Purchase Orders Module

Purchase orders and supplier management.

## Features

- Create and manage purchase orders with full lifecycle tracking (draft, sent, confirmed, received, cancelled)
- Maintain a supplier directory with contact details and tax ID
- Line-item detail per order with quantity, unit price, and automatic totals
- Track order subtotals, tax amounts, and grand totals
- Set expected delivery dates on orders
- Add notes to orders and suppliers

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Purchase Orders > Settings**

## Usage

Access via: **Menu > Purchase Orders**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/purchase_orders/dashboard/` | Overview of purchase order activity |
| Orders | `/m/purchase_orders/orders/` | List and manage purchase orders |
| Suppliers | `/m/purchase_orders/suppliers/` | Manage supplier directory |
| Settings | `/m/purchase_orders/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `Supplier` | Supplier with name, email, phone, address, tax ID, and active status |
| `PurchaseOrder` | Purchase order linked to a supplier with order number, status, dates, and monetary totals |
| `PurchaseOrderLine` | Individual line item within a purchase order with description, quantity, unit price, and total |

## Permissions

| Permission | Description |
|------------|-------------|
| `purchase_orders.view_purchaseorder` | View purchase orders |
| `purchase_orders.add_purchaseorder` | Create new purchase orders |
| `purchase_orders.change_purchaseorder` | Edit existing purchase orders |
| `purchase_orders.delete_purchaseorder` | Delete purchase orders |
| `purchase_orders.view_supplier` | View suppliers |
| `purchase_orders.add_supplier` | Create new suppliers |
| `purchase_orders.change_supplier` | Edit existing suppliers |
| `purchase_orders.delete_supplier` | Delete suppliers |
| `purchase_orders.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
