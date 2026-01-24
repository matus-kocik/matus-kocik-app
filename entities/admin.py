from django.contrib import admin
from .models import Entity, BankAccount


class BankAccountInline(admin.TabularInline):
    """
    Inline admin for managing bank accounts directly on the entity detail page.
    """
    model = BankAccount
    extra = 1
    autocomplete_fields = ("entity",)
    fields = ("iban", "swift", "is_default")
    ordering = ("-is_default",)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    """
    Admin configuration for business entities (supplier / customer).
    Focuses on quick search, clean overview, and inline bank account management.
    """

    list_display = ("name", "ico", "dic", "ic_dph", "city", "country")
    list_display_links = ("name",)
    search_fields = ("name", "ico", "dic", "ic_dph", "email")
    list_filter = ("country",)
    ordering = ("name",)

    fieldsets = (
        (
            "Základné údaje",
            {
                "fields": (
                    "name",
                    "email",
                )
            },
        ),
        (
            "Identifikácia",
            {
                "fields": (
                    "ico",
                    "dic",
                    "ic_dph",
                )
            },
        ),
        (
            "Adresa",
            {
                "fields": (
                    "street",
                    "zip_code",
                    "city",
                    "country",
                )
            },
        ),
    )

    inlines = [BankAccountInline]


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    """
    Standalone admin for bank accounts.
    Mostly useful for debugging or bulk inspection.
    """

    list_display = ("iban", "entity", "is_default")
    list_filter = ("is_default",)
    search_fields = ("iban", "entity__name")
    autocomplete_fields = ("entity",)
    ordering = ("entity", "-is_default")
