# URL configuration for the entities app.
# Keeps routing simple and mirrors basic entity management workflows.

from django.urls import path

from .views import (
    EntityListView,
    EntityCreateView,
    EntityUpdateView,
    EntityDeleteView,
)

app_name = "entities"

urlpatterns = [
    # Entity list / overview
    path("", EntityListView.as_view(), name="entity_list"),
    # Create a new entity
    path("new/", EntityCreateView.as_view(), name="entity_create"),
    # Edit an existing entity
    path("<int:pk>/update/", EntityUpdateView.as_view(), name="entity_update"),
    # Delete an entity
    path("<int:pk>/delete/", EntityDeleteView.as_view(), name="entity_delete"),
]