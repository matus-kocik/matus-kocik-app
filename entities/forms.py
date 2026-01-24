"""
This module defines presentation-only Django ModelForms for the entities app.
It mirrors the styling contract used in invoices/forms.py to ensure visual consistency
across the application. All forms here must stay visually consistent with the rest of the app.
"""

from django import forms

from .models import Entity, BankAccount


# Shared UI contract for form inputs; intentionally matches invoices.forms.BASE_INPUT_CLASS
BASE_INPUT_CLASS = "w-full rounded-xl bg-white/80 text-[#003D5B] px-4 py-3 placeholder:text-[#003D5B]/60 focus:outline-none focus:ring-2 focus:ring-[#EDAE49]"


class EntityForm(forms.ModelForm):
    """
    Presentation-focused form for creating and editing business entities (supplier / customer).
    This form defines widgets and CSS classes only, with no business logic or validation beyond
    basic Django defaults. It is designed for reuse across invoices, entities CRUD, profile, and future flows.
    """

    class Meta:
        model = Entity
        fields = [
            "name",
            "ico",
            "dic",
            "ic_dph",
            "street",
            "zip_code",
            "city",
            "country",
            "email",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "ico": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "dic": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "ic_dph": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "street": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "zip_code": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "city": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "country": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "email": forms.EmailInput(attrs={"class": BASE_INPUT_CLASS}),
        }


class BankAccountForm(forms.ModelForm):
    """
    Presentation-only form for managing bank accounts linked to an entity.
    Typically used inline or as a secondary step associated with an Entity.
    """

    class Meta:
        model = BankAccount
        fields = ["iban", "swift", "is_default"]
        widgets = {
            "iban": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "swift": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "is_default": forms.CheckboxInput(attrs={"class": "rounded text-[#EDAE49] focus:ring-[#EDAE49]"}),
        }
