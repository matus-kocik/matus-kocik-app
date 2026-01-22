from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.db import transaction
from django.shortcuts import redirect

from .models import Invoice
from .forms import InvoiceForm, InvoiceItemFormSet
from django.utils import timezone


class InvoiceListView(ListView):
    model = Invoice
    template_name = "invoices/invoice_list.html"
    context_object_name = "invoices"

    def get_queryset(self):
        return Invoice.objects.filter(is_deleted=False).order_by("-created_at")


class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoices/invoice_form.html"
    success_url = reverse_lazy("invoice_list")

    def get_initial(self):
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
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = InvoiceItemFormSet(self.request.POST)
        else:
            context["formset"] = InvoiceItemFormSet()
        context["invoice_number"] = self.get_initial().get("number")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        with transaction.atomic():
            if not form.instance.number:
                form.instance.number = self.get_initial().get("number")
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                self.object.recalculate_total()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class InvoiceUpdateView(UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoices/invoice_form.html"
    success_url = reverse_lazy("invoice_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = InvoiceItemFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["formset"] = InvoiceItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
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
    model = Invoice
    template_name = "invoices/invoice_confirm_delete.html"
    success_url = reverse_lazy("invoice_list")

    def delete(self, request, *args, **kwargs):
        invoice = self.get_object()
        invoice.is_deleted = True
        invoice.save(update_fields=["is_deleted"])
        return redirect(self.success_url)
