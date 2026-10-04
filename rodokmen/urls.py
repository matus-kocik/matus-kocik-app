from django.urls import path

from .views import RodokmenView

app_name = "rodokmen"

urlpatterns = [
    path("", RodokmenView.as_view(), name="rodokmen"),
]
