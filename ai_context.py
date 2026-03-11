"""
AI context for the Purchase Orders module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Purchase Orders

### Models

**Supplier**
- `name` (str, required), `email`, `phone`, `address` (text), `tax_id`, `notes`, `is_active` (bool)
- Represents a vendor from whom goods are purchased.

**PurchaseOrder**
- `order_number` (str, unique, required), `supplier` (FK → Supplier, CASCADE)
- `status` choices: draft | sent | confirmed | received | cancelled (default: draft)
- `expected_date` (date, optional), `subtotal`, `tax_amount`, `total` (decimals, default 0)
- `notes` (text)

**PurchaseOrderLine**
- `order` (FK → PurchaseOrder, CASCADE, related_name='lines')
- `description` (str), `quantity` (decimal, default 1), `unit_price` (decimal), `total` (decimal)
- total = quantity × unit_price (must be set explicitly; not auto-calculated).

### Key Flows

1. **Create supplier**: provide name plus optional contact details.
2. **Create PO**: set order_number (unique), link supplier, set expected_date if known. Status starts as 'draft'.
3. **Add lines**: create PurchaseOrderLine records linked to the PO with description, quantity, unit_price, and total.
4. **Update PO totals**: after adding lines, update PO subtotal, tax_amount, and total accordingly.
5. **Progress status**: draft → sent → confirmed → received. Cancel at any stage with 'cancelled'.

### Relationships

- PurchaseOrderLine → PurchaseOrder (CASCADE). Access via `order.lines.all()`.
- PurchaseOrder → Supplier (CASCADE).
- No direct FK to inventory/products — lines use free-text description.
"""
