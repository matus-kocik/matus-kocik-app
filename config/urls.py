# Root URL configuration for the project.
# Defines entry points and delegates app-specific routing.
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

if settings.DEBUG:
    admin_url = "admin/"
else:
    admin_url = getattr(settings, "ADMIN_URL", "admin/")

# Top-level URL routes
urlpatterns = [
    # Django admin interface
    path(admin_url, admin.site.urls),
    # Public home / landing page
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    # Users application routes
    path("", include("users.urls")),
    # Invoices application routes
    path("invoices/", include("invoices.urls")),
    # Entities application routes
    path("entities/", include("entities.urls")),
    path("blog/", include("blog.urls")),
    path("tinymce/", include("tinymce.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
