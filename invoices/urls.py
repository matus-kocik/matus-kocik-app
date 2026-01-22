

from django.urls import path

from .views import (
    InvoiceListView,
    InvoiceCreateView,
    InvoiceUpdateView,
    InvoiceDeleteView,
)

urlpatterns = [
    path("", InvoiceListView.as_view(), name="invoice_list"),
    path("new/", InvoiceCreateView.as_view(), name="invoice_create"),
    path("<int:pk>/edit/", InvoiceUpdateView.as_view(), name="invoice_edit"),
    path("<int:pk>/delete/", InvoiceDeleteView.as_view(), name="invoice_delete"),
]