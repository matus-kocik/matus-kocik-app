# Views for managing business entities (suppliers / customers).
# These views provide basic CRUD operations for reusable entities
# that can later be referenced from invoices and other modules.

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from urllib.parse import urlparse, urlunparse
from django.http import QueryDict

from .models import Entity
from .forms import EntityForm


class EntityListView(LoginRequiredMixin, ListView):
    """
    List view showing all business entities.
    Acts as a central directory for suppliers and customers.
    """
    model = Entity
    template_name = "entities/entity_list.html"
    context_object_name = "entities"

    def get_queryset(self):
        return Entity.objects.filter(owner=self.request.user)


class EntityCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new business entity.
    Used when adding a new supplier or customer.
    """
    model = Entity
    form_class = EntityForm
    template_name = "entities/entity_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()

        next_url = self.request.GET.get("next")
        field_name = self.request.GET.get("field")

        if next_url:
            parts = urlparse(next_url)
            query = QueryDict(parts.query, mutable=True)

            # Preserve original values coming from the invoice form
            supplier_id = self.request.GET.get("supplier")
            customer_id = self.request.GET.get("customer")

            if supplier_id:
                query["supplier"] = supplier_id
            if customer_id:
                query["customer"] = customer_id

            # Assign the newly created entity to the correct field
            if field_name:
                query[field_name] = str(self.object.pk)

            return redirect(
                urlunparse(parts._replace(query=query.urlencode()))
            )

        return super().form_valid(form)


class EntityUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an existing business entity.
    Allows editing of identification and address details.
    """
    model = Entity
    form_class = EntityForm
    template_name = "entities/entity_form.html"
    success_url = reverse_lazy("entities:entity_list")

    def get_queryset(self):
        return Entity.objects.filter(owner=self.request.user)


class EntityDeleteView(LoginRequiredMixin, DeleteView):
    """
    Permanently delete a business entity.
    (Later can be changed to soft-delete if needed.)
    """
    model = Entity
    template_name = "entities/entity_confirm_delete.html"
    success_url = reverse_lazy("entities:entity_list")

    def get_queryset(self):
        return Entity.objects.filter(owner=self.request.user)