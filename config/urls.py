# Root URL configuration for the project.
# Defines entry points and delegates app-specific routing.
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# Top-level URL routes
urlpatterns = [
    # Django admin interface
    path("admin/", admin.site.urls),
    # Public home / landing page
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    # Invoices application routes
    path("invoices/", include("invoices.urls")),
]
