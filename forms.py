from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Supplier, PurchaseOrderLine

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'address', 'tax_id', 'notes', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'email': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'address': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'tax_id': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class PurchaseOrderLineForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderLine
        fields = ['order', 'description', 'quantity', 'unit_price', 'total']
        widgets = {
            'order': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'description': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'quantity': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'unit_price': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'total': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

