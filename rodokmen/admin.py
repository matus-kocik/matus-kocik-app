from django.contrib import admin

from .models import Connection, Node


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "node_type",
        "year_from",
        "year_to",
        "period_label",
        "is_published",
        "order",
    )

    list_filter = (
        "node_type",
        "is_published",
    )

    search_fields = (
        "name",
        "period_label",
        "short_description",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "order",
        "year_from",
        "name",
    )

    fieldsets = (
        (
            "Základné údaje",
            {
                "fields": (
                    "name",
                    "slug",
                    "node_type",
                ),
            },
        ),
        (
            "Časové zaradenie",
            {
                "fields": (
                    "year_from",
                    "year_to",
                    "period_label",
                ),
                "description": (
                    "Roky používame na chronologické zoradenie a časovú os. "
                    "Označenie obdobia sa môže zobrazovať namiesto rokov, "
                    "napr. „18. storočie“ alebo „stredovek“."
                ),
            },
        ),
        (
            "Obsah",
            {
                "fields": (
                    "short_description",
                    "description",
                    "editor_note",
                ),
                "description": (
                    "Poznámka redaktora slúži na transparentné označenie "
                    "redakčných alebo orientačných doplnení, ktoré nie sú "
                    "priamo prevzaté zo zdrojovej literatúry."
                ),
            },
        ),
        (
            "Zobrazenie",
            {
                "fields": (
                    "order",
                    "is_published",
                    "published_at",
                ),
            },
        ),
    )


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = (
        "source",
        "connection_type",
        "target",
        "is_published",
        "order",
    )

    list_filter = (
        "connection_type",
        "is_published",
    )

    search_fields = (
        "name",
        "period_label",
        "short_description",
        "description",
        "editor_note",
    )

    autocomplete_fields = (
        "source",
        "target",
    )

    ordering = (
        "order",
        "id",
    )

    fieldsets = (
        (
            "Prepojenie",
            {
                "fields": (
                    "source",
                    "connection_type",
                    "target",
                ),
            },
        ),
        (
            "Popis",
            {
                "fields": ("description",),
            },
        ),
        (
            "Zobrazenie",
            {
                "fields": (
                    "order",
                    "is_published",
                    "published_at",
                ),
            },
        ),
    )
