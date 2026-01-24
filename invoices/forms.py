# Forms for creating and editing invoices and their line items.
# Focused mainly on presentation (widgets, CSS classes), not business logic.
from django import forms
from django.forms import inlineformset_factory

from .models import Invoice, InvoiceItem


# Shared Tailwind CSS classes for form inputs.
# Centralized here to keep widget definitions consistent and maintainable.
BASE_INPUT_CLASS = "w-full rounded-xl bg-white/80 text-[#003D5B] px-4 py-3 placeholder:text-[#003D5B]/60 focus:outline-none focus:ring-2 focus:ring-[#EDAE49]"
BASE_INPUT_NUMBER_CLASS = BASE_INPUT_CLASS + " text-right"


class InvoiceForm(forms.ModelForm):
    """
    Model form for creating and editing invoices.
    Handles only field presentation and basic HTML input configuration.
    """
    class Meta:
        """
        Meta configuration mapping Invoice model fields to form widgets.
        """
        model = Invoice
        fields = "__all__"
        widgets = {
            "number": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "issue_date": forms.DateInput(attrs={
                "type": "date",
                "class": BASE_INPUT_CLASS
            }),
            "delivery_date": forms.DateInput(attrs={
                "type": "date",
                "class": BASE_INPUT_CLASS
            }),
            "due_date": forms.DateInput(attrs={
                "type": "date",
                "class": BASE_INPUT_CLASS
            }),

            # Supplier (issuer)
            "supplier_name": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "supplier_ico": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "supplier_dic": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "supplier_iban": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS + " font-mono"
            }),

            # Customer
            "customer_name": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "customer_ico": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "customer_dic": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "customer_ic_dph": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "customer_street": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "customer_street_number": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "customer_city": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "customer_zip": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "customer_country": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "customer_email": forms.EmailInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "customer_iban": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS + " font-mono"
            }),

            # Payment details
            "variable_symbol": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "constant_symbol": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "specific_symbol": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),

            # Additional note
            "note": forms.Textarea(attrs={
                "class": BASE_INPUT_CLASS,
                "rows": 4
            }),
        }


class InvoiceItemForm(forms.ModelForm):
    """
    Form for a single invoice line item.
    Used primarily within an inline formset.
    """
    class Meta:
        """
        Meta configuration for invoice item fields and widgets.
        """
        model = InvoiceItem
        fields = ("name", "quantity", "unit_price")
        widgets = {
            "name": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASS
            }),
            "quantity": forms.NumberInput(attrs={
                "class": BASE_INPUT_NUMBER_CLASS,
                "step": "any",
                "min": "0"
            }),
            "unit_price": forms.NumberInput(attrs={
                "class": BASE_INPUT_NUMBER_CLASS + " font-mono",
                "step": "any",
                "min": "0"
            }),
        }


# Inline formset for managing invoice items directly within the invoice form.
InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True,
)
