from django.views.generic import TemplateView

from .models import Connection, Node


class RodokmenView(TemplateView):
    template_name = "rodokmen/rodokmen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        nodes = Node.objects.filter(
            is_published=True,
        ).order_by(
            "order",
            "year_from",
            "name",
        )

        connections = (
            Connection.objects.filter(
                is_published=True,
                source__is_published=True,
                target__is_published=True,
            )
            .select_related(
                "source",
                "target",
            )
            .order_by(
                "order",
                "id",
            )
        )

        context["nodes"] = [
            {
                "id": node.id,
                "name": node.name,
                "slug": node.slug,
                "node_type": node.node_type,
                "node_type_display": node.get_node_type_display(),
                "year_from": node.year_from,
                "year_to": node.year_to,
                "period_label": node.period_label,
                "short_description": node.short_description,
                "description": node.description,
            }
            for node in nodes
        ]

        context["connections"] = [
            {
                "id": connection.id,
                "source": connection.source_id,
                "target": connection.target_id,
                "connection_type": connection.connection_type,
                "connection_type_display": (connection.get_connection_type_display()),
                "description": connection.description,
            }
            for connection in connections
        ]

        return context
