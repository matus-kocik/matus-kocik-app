# Views for managing invoices (CRUD + PDF export).
# Views handle HTTP flow and orchestration; business logic lives in models.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.db import transaction
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from .models import Invoice
from .forms import InvoiceForm, InvoiceItemFormSet
from django.utils import timezone


class InvoiceListView(ListView):
    """
    List view showing all non-deleted invoices.
    Acts as the main overview screen.
    """
    model = Invoice
    template_name = "invoices/invoice_list.html"
    context_object_name = "invoices"

    def get_queryset(self):
        """
        Exclude soft-deleted invoices and show newest first.
        """
        return Invoice.objects.filter(is_deleted=False).order_by("-created_at")


class InvoiceCreateView(CreateView):
    """
    Create view for a new invoice together with its line items.
    Handles invoice number generation and atomic save of invoice + items.
    """
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoices/invoice_form.html"
    success_url = reverse_lazy("invoice_list")

    def get_initial(self):
        """
        Pre-fill invoice number based on the current year and last used sequence.
        """
        initial = super().get_initial()
        year = timezone.now().year
        last_invoice = (
            Invoice.objects.filter(number__startswith=str(year))
            .order_by("-number")
            .first()
        )

        if last_invoice:
            last_seq = int(last_invoice.number[-4:])
            next_seq = last_seq + 1
        else:
            next_seq = 1

        initial["number"] = f"{year}{next_seq:04d}"
        return initial

    def get_context_data(self, **kwargs):
        """
        Attach the invoice item formset to the template context.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = InvoiceItemFormSet(self.request.POST)
        else:
            context["formset"] = InvoiceItemFormSet()
        context["invoice_number"] = self.get_initial().get("number")
        return context

    def form_valid(self, form):
        """
        Save invoice and related items in a single database transaction.
        """
        context = self.get_context_data()
        formset = context["formset"]

        with transaction.atomic():
            self.object = form.save()

            # Save invoice first; save items only if the formset is valid and not empty
            if formset.is_valid() and formset.has_changed():
                formset.instance = self.object
                formset.save()

            self.object.recalculate_total()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.success_url


class InvoiceUpdateView(UpdateView):
    """
    Update view for an existing invoice and its items.
    """
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoices/invoice_form.html"
    success_url = reverse_lazy("invoice_list")

    def get_context_data(self, **kwargs):
        """
        Bind the invoice item formset to the existing invoice.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = InvoiceItemFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["formset"] = InvoiceItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """
        Persist invoice changes and synchronize item totals atomically.
        """
        context = self.get_context_data()
        formset = context["formset"]

        with transaction.atomic():
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                self.object.recalculate_total()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class InvoiceDeleteView(DeleteView):
    """
    Soft-delete view that hides an invoice without removing it from the database.
    """
    model = Invoice
    template_name = "invoices/invoice_confirm_delete.html"
    success_url = reverse_lazy("invoice_list")

    def delete(self, request, *args, **kwargs):
        """
        Mark invoice as deleted instead of performing a hard delete.
        """
        invoice = self.get_object()
        invoice.is_deleted = True
        invoice.save(update_fields=["is_deleted"])
        return redirect(self.success_url)


class InvoicePDFView(DetailView):
    """
    Render an invoice as a PDF document using an HTML template.
    """
    model = Invoice

    def get(self, request, *args, **kwargs):
        """
        Generate and return the invoice PDF as an inline HTTP response.
        """
        invoice = self.get_object()
        html_string = render_to_string(
            "invoices/pdf/invoice.html",
            {"invoice": invoice}
        )
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="invoice_{invoice.number}.pdf"'
        return response
