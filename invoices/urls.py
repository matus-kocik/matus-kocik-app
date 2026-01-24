# URL configuration for the invoices app.
# Keeps routing simple and mirrors the main user workflows.

from django.urls import path

from .views import (
    InvoiceListView,
    InvoiceCreateView,
    InvoiceUpdateView,
    InvoiceDeleteView,
    InvoicePDFView,
)

urlpatterns = [
    # Invoice list / dashboard
    path("", InvoiceListView.as_view(), name="invoice_list"),
    # Create a new invoice
    path("new/", InvoiceCreateView.as_view(), name="invoice_create"),
    # Edit an existing invoice
    path("<int:pk>/edit/", InvoiceUpdateView.as_view(), name="invoice_edit"),
    # Soft-delete an invoice
    path("<int:pk>/delete/", InvoiceDeleteView.as_view(), name="invoice_delete"),
    # Render invoice as PDF
    path("<int:pk>/pdf/", InvoicePDFView.as_view(), name="invoice_pdf"),
]
