"""AI tools for the Purchase Orders module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListPurchaseOrders(AssistantTool):
    name = "list_purchase_orders"
    description = "List purchase orders with optional filters."
    module_id = "purchase_orders"
    required_permission = "purchase_orders.view_purchaseorder"
    parameters = {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Filter: draft, sent, confirmed, received, cancelled"},
            "supplier_id": {"type": "string", "description": "Filter by supplier ID"},
            "limit": {"type": "integer", "description": "Max results (default 20)"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from purchase_orders.models import PurchaseOrder
        qs = PurchaseOrder.objects.select_related('supplier').order_by('-order_date')
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        if args.get('supplier_id'):
            qs = qs.filter(supplier_id=args['supplier_id'])
        limit = args.get('limit', 20)
        return {
            "purchase_orders": [
                {
                    "id": str(po.id),
                    "order_number": po.order_number,
                    "supplier": po.supplier.name if po.supplier else None,
                    "status": po.status,
                    "total": str(po.total),
                    "order_date": str(po.order_date) if po.order_date else None,
                    "expected_date": str(po.expected_date) if po.expected_date else None,
                }
                for po in qs[:limit]
            ],
            "total": qs.count(),
        }


@register_tool
class CreatePurchaseOrder(AssistantTool):
    name = "create_purchase_order"
    description = "Create a new purchase order for a supplier."
    module_id = "purchase_orders"
    required_permission = "purchase_orders.change_purchaseorder"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "supplier_id": {"type": "string", "description": "Supplier ID"},
            "notes": {"type": "string", "description": "Order notes"},
            "expected_date": {"type": "string", "description": "Expected delivery date (YYYY-MM-DD)"},
            "lines": {
                "type": "array",
                "description": "Order lines",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "string"},
                    },
                    "required": ["description", "quantity", "unit_price"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["supplier_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from datetime import date
        from decimal import Decimal
        from purchase_orders.models import PurchaseOrder, PurchaseOrderLine
        po = PurchaseOrder.objects.create(
            supplier_id=args['supplier_id'],
            notes=args.get('notes', ''),
            expected_date=args.get('expected_date'),
            order_date=date.today(),
            status='draft',
        )
        for line in args.get('lines', []):
            PurchaseOrderLine.objects.create(
                order=po,
                description=line['description'],
                quantity=line['quantity'],
                unit_price=Decimal(line['unit_price']),
            )
        po.save()
        return {"id": str(po.id), "order_number": po.order_number, "created": True}


@register_tool
class ListSuppliers(AssistantTool):
    name = "list_suppliers"
    description = "List suppliers."
    module_id = "purchase_orders"
    required_permission = "purchase_orders.view_purchaseorder"
    parameters = {
        "type": "object",
        "properties": {
            "search": {"type": "string", "description": "Search by name"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from purchase_orders.models import Supplier
        qs = Supplier.objects.filter(is_active=True)
        if args.get('search'):
            qs = qs.filter(name__icontains=args['search'])
        return {
            "suppliers": [
                {"id": str(s.id), "name": s.name, "email": s.email, "phone": s.phone}
                for s in qs[:50]
            ]
        }
