# Views for managing business entities (suppliers / customers).
# These views provide basic CRUD operations for reusable entities
# that can later be referenced from invoices and other modules.

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Entity
from .forms import EntityForm


class EntityListView(ListView):
    """
    List view showing all business entities.
    Acts as a central directory for suppliers and customers.
    """
    model = Entity
    template_name = "entities/entity_list.html"
    context_object_name = "entities"


class EntityCreateView(CreateView):
    """
    Create a new business entity.
    Used when adding a new supplier or customer.
    """
    model = Entity
    form_class = EntityForm
    template_name = "entities/entity_form.html"
    success_url = reverse_lazy("entities:entity_list")


class EntityUpdateView(UpdateView):
    """
    Update an existing business entity.
    Allows editing of identification and address details.
    """
    model = Entity
    form_class = EntityForm
    template_name = "entities/entity_form.html"
    success_url = reverse_lazy("entities:entity_list")


class EntityDeleteView(DeleteView):
    """
    Permanently delete a business entity.
    (Later can be changed to soft-delete if needed.)
    """
    model = Entity
    template_name = "entities/entity_confirm_delete.html"
    success_url = reverse_lazy("entities:entity_list")