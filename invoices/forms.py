# Forms for creating and editing invoices and their line items.
# Focused mainly on presentation (widgets, CSS classes), not business logic.
from django import forms
from django.forms import inlineformset_factory

from entities.models import Entity

from .models import Invoice, InvoiceItem

# Shared Tailwind CSS classes for form inputs.
# Centralized here to keep widget definitions consistent and maintainable.
BASE_INPUT_CLASS = "w-full rounded-xl bg-white/90 text-[#003D5B] px-4 py-3 placeholder:text-[#003D5B]/60 focus:outline-none focus:ring-2 focus:ring-[#EDAE49]"
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
        fields = (
            "number",
            "issue_date",
            "delivery_date",
            "due_date",
            "supplier",
            "customer",
            "variable_symbol",
            "constant_symbol",
            "specific_symbol",
            "note",
        )
        widgets = {
            "number": forms.TextInput(attrs={"class": BASE_INPUT_CLASS, "readonly": "readonly"}),
            "issue_date": forms.DateInput(
                attrs={"type": "date", "class": BASE_INPUT_CLASS}
            ),
            "delivery_date": forms.DateInput(
                attrs={"type": "date", "class": BASE_INPUT_CLASS}
            ),
            "due_date": forms.DateInput(
                attrs={"type": "date", "class": BASE_INPUT_CLASS}
            ),
            "supplier": forms.Select(attrs={"class": BASE_INPUT_CLASS}),
            "customer": forms.Select(attrs={"class": BASE_INPUT_CLASS}),
            "variable_symbol": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "constant_symbol": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "specific_symbol": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "note": forms.Textarea(attrs={"class": BASE_INPUT_CLASS, "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["supplier"].queryset = Entity.objects.filter(owner=user)
            self.fields["customer"].queryset = Entity.objects.filter(owner=user)


class InvoiceItemForm(forms.ModelForm):
    def clean_quantity(self):
        value = self.cleaned_data.get("quantity")
        if value is not None and value <= 0:
            raise forms.ValidationError("Množstvo musí byť väčšie ako 0.")
        return value

    def clean_unit_price(self):
        value = self.cleaned_data.get("unit_price")
        if value is not None and value < 0:
            raise forms.ValidationError("Cena nemôže byť záporná.")
        return value
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
            "name": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "quantity": forms.NumberInput(
                attrs={"class": BASE_INPUT_NUMBER_CLASS, "step": "any", "min": "0"}
            ),
            "unit_price": forms.NumberInput(
                attrs={
                    "class": BASE_INPUT_NUMBER_CLASS + " font-mono",
                    "step": "any",
                    "min": "0",
                }
            ),
        }


# Inline formset for managing invoice items directly within the invoice form.
InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
