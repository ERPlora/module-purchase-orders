"""Tests for purchase_orders models."""
import pytest
from django.utils import timezone

from purchase_orders.models import Supplier, PurchaseOrderLine


@pytest.mark.django_db
class TestSupplier:
    """Supplier model tests."""

    def test_create(self, supplier):
        """Test Supplier creation."""
        assert supplier.pk is not None
        assert supplier.is_deleted is False

    def test_str(self, supplier):
        """Test string representation."""
        assert str(supplier) is not None
        assert len(str(supplier)) > 0

    def test_soft_delete(self, supplier):
        """Test soft delete."""
        pk = supplier.pk
        supplier.is_deleted = True
        supplier.deleted_at = timezone.now()
        supplier.save()
        assert not Supplier.objects.filter(pk=pk).exists()
        assert Supplier.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, supplier):
        """Test default queryset excludes deleted."""
        supplier.is_deleted = True
        supplier.deleted_at = timezone.now()
        supplier.save()
        assert Supplier.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, supplier):
        """Test toggling is_active."""
        original = supplier.is_active
        supplier.is_active = not original
        supplier.save()
        supplier.refresh_from_db()
        assert supplier.is_active != original


@pytest.mark.django_db
class TestPurchaseOrderLine:
    """PurchaseOrderLine model tests."""

    def test_create(self, purchase_order_line):
        """Test PurchaseOrderLine creation."""
        assert purchase_order_line.pk is not None
        assert purchase_order_line.is_deleted is False

    def test_soft_delete(self, purchase_order_line):
        """Test soft delete."""
        pk = purchase_order_line.pk
        purchase_order_line.is_deleted = True
        purchase_order_line.deleted_at = timezone.now()
        purchase_order_line.save()
        assert not PurchaseOrderLine.objects.filter(pk=pk).exists()
        assert PurchaseOrderLine.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, purchase_order_line):
        """Test default queryset excludes deleted."""
        purchase_order_line.is_deleted = True
        purchase_order_line.deleted_at = timezone.now()
        purchase_order_line.save()
        assert PurchaseOrderLine.objects.filter(hub_id=hub_id).count() == 0


