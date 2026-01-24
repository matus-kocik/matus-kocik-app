from django.contrib import admin

from .models import Invoice, InvoiceItem


# Admin configuration for invoices.
# This file intentionally contains only configuration (no business logic).


class InvoiceItemInline(admin.TabularInline):
    """
    Inline configuration for invoice line items.
    Allows editing items directly on the invoice admin page.
    """
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Invoice.
    Focused on clarity and safe editing.
    """
    list_display = (
        "number",
        "supplier",
        "customer",
        "issue_date",
        "due_date",
        "total",
        "is_deleted",
    )
    list_filter = ("is_deleted", "issue_date", "due_date")
    search_fields = ("number", "customer__name", "supplier__name")
    ordering = ("-created_at",)

    inlines = [InvoiceItemInline]

    readonly_fields = ("total", "created_at")

    fieldsets = (
        (
            "Invoice",
            {
                "fields": (
                    "number",
                    "issue_date",
                    "delivery_date",
                    "due_date",
                )
            },
        ),
        (
            "Entities",
            {
                "fields": (
                    "supplier",
                    "customer",
                )
            },
        ),
        (
            "Payment",
            {
                "fields": (
                    "bank_account",
                    "variable_symbol",
                    "constant_symbol",
                    "specific_symbol",
                )
            },
        ),
        (
            "Additional",
            {
                "fields": (
                    "note",
                    "is_deleted",
                )
            },
        ),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for standalone invoice item view.
    Mostly useful for debugging; items are usually edited inline.
    """
    list_display = ("name", "invoice", "quantity", "unit_price", "total")
    search_fields = ("name",)
    ordering = ("invoice",)