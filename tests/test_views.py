"""Tests for purchase_orders views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('purchase_orders:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('purchase_orders:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('purchase_orders:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSupplierViews:
    """Supplier view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('purchase_orders:suppliers_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('purchase_orders:suppliers_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('purchase_orders:suppliers_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('purchase_orders:suppliers_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('purchase_orders:suppliers_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('purchase_orders:suppliers_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('purchase_orders:supplier_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('purchase_orders:supplier_add')
        data = {
            'name': 'New Name',
            'email': 'test@example.com',
            'phone': 'New Phone',
            'address': 'Test description',
            'tax_id': 'New Tax Id',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, supplier):
        """Test edit form loads."""
        url = reverse('purchase_orders:supplier_edit', args=[supplier.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, supplier):
        """Test editing via POST."""
        url = reverse('purchase_orders:supplier_edit', args=[supplier.pk])
        data = {
            'name': 'Updated Name',
            'email': 'test@example.com',
            'phone': 'Updated Phone',
            'address': 'Test description',
            'tax_id': 'Updated Tax Id',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, supplier):
        """Test soft delete via POST."""
        url = reverse('purchase_orders:supplier_delete', args=[supplier.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        supplier.refresh_from_db()
        assert supplier.is_deleted is True

    def test_toggle_status(self, auth_client, supplier):
        """Test toggle active status."""
        url = reverse('purchase_orders:supplier_toggle_status', args=[supplier.pk])
        original = supplier.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        supplier.refresh_from_db()
        assert supplier.is_active != original

    def test_bulk_delete(self, auth_client, supplier):
        """Test bulk delete."""
        url = reverse('purchase_orders:suppliers_bulk_action')
        response = auth_client.post(url, {'ids': str(supplier.pk), 'action': 'delete'})
        assert response.status_code == 200
        supplier.refresh_from_db()
        assert supplier.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('purchase_orders:suppliers_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestPurchaseOrderLineViews:
    """PurchaseOrderLine view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('purchase_orders:purchase_order_lines_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('purchase_orders:purchase_order_lines_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('purchase_orders:purchase_order_lines_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('purchase_orders:purchase_order_lines_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('purchase_orders:purchase_order_lines_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('purchase_orders:purchase_order_lines_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('purchase_orders:purchase_order_line_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('purchase_orders:purchase_order_line_add')
        data = {
            'description': 'New Description',
            'quantity': '100.00',
            'unit_price': '100.00',
            'total': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, purchase_order_line):
        """Test edit form loads."""
        url = reverse('purchase_orders:purchase_order_line_edit', args=[purchase_order_line.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, purchase_order_line):
        """Test editing via POST."""
        url = reverse('purchase_orders:purchase_order_line_edit', args=[purchase_order_line.pk])
        data = {
            'description': 'Updated Description',
            'quantity': '100.00',
            'unit_price': '100.00',
            'total': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, purchase_order_line):
        """Test soft delete via POST."""
        url = reverse('purchase_orders:purchase_order_line_delete', args=[purchase_order_line.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        purchase_order_line.refresh_from_db()
        assert purchase_order_line.is_deleted is True

    def test_bulk_delete(self, auth_client, purchase_order_line):
        """Test bulk delete."""
        url = reverse('purchase_orders:purchase_order_lines_bulk_action')
        response = auth_client.post(url, {'ids': str(purchase_order_line.pk), 'action': 'delete'})
        assert response.status_code == 200
        purchase_order_line.refresh_from_db()
        assert purchase_order_line.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('purchase_orders:purchase_order_lines_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('purchase_orders:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('purchase_orders:settings')
        response = client.get(url)
        assert response.status_code == 302

