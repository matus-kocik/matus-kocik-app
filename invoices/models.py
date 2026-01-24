from django.db import models
from decimal import Decimal


class Invoice(models.Model):
    """
    Represents a sales invoice including supplier, customer, and payment details.
    Acts as the aggregate root for invoice items.
    """
    # Core invoice identification and dates
    number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Číslo faktúry",
    )

    issue_date = models.DateField(verbose_name="Dátum vystavenia")
    due_date = models.DateField(verbose_name="Dátum splatnosti")

    delivery_date = models.DateField(
        verbose_name="Dátum dodania",
    )

    supplier_iban = models.CharField(
        max_length=34,
        verbose_name="IBAN dodávateľa",
    )

    customer_iban = models.CharField(
        max_length=34,
        blank=True,
        verbose_name="IBAN odberateľa",
    )

    # Payment identifiers used mainly for bank transfers (SK/CZ context)
    variable_symbol = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Variabilný symbol",
    )

    constant_symbol = models.CharField(
        max_length=4,
        default="0308",
        verbose_name="Konštantný symbol",
    )

    specific_symbol = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Špecifický symbol",
    )

    # Supplier (issuer) identification
    supplier_name = models.CharField(
        max_length=255,
        verbose_name="Názov dodávateľa",
    )
    supplier_ico = models.CharField(
        max_length=20,
        verbose_name="IČO dodávateľa",
    )
    supplier_dic = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="DIČ dodávateľa",
    )

    # Customer identification and address
    customer_name = models.CharField(
        max_length=255,
        verbose_name="Obchodné meno / meno a priezvisko",
    )

    customer_ico = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="IČO",
    )

    customer_dic = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="DIČ",
    )

    customer_ic_dph = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="IČ DPH",
    )

    customer_street = models.CharField(
        max_length=255,
        verbose_name="Ulica",
    )

    customer_street_number = models.CharField(
        max_length=50,
        verbose_name="Číslo",
    )

    customer_city = models.CharField(
        max_length=100,
        verbose_name="Mesto",
    )

    customer_zip = models.CharField(
        max_length=10,
        verbose_name="PSČ",
    )

    customer_country = models.CharField(
        max_length=100,
        verbose_name="Krajina",
    )

    customer_email = models.EmailField(
        blank=True,
        verbose_name="Email odberateľa",
    )

    note = models.TextField(
        blank=True,
        verbose_name="Poznámka",
    )

    # Cached total amount of the invoice (calculated from items)
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False,
        verbose_name="Celková suma",
    )

    # Soft-delete flag to keep invoices for history/audit purposes
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Zmazaná",
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Vytvorené",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Aktualizované",
    )

    def recalculate_total(self):
        """
        Recalculate and persist the invoice total based on related items.
        """
        total = sum(
            (item.total for item in self.items.all()),
            Decimal("0"),
        )
        Invoice.objects.filter(pk=self.pk).update(total=total)

    def save(self, *args, **kwargs):
        """
        Ensure variable symbol defaults to invoice number on first save.
        """
        if not self.variable_symbol:
            self.variable_symbol = self.number
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation used in admin and selections.
        """
        return self.number


class InvoiceItem(models.Model):
    """
    Line item belonging to an invoice.
    Calculates its own total and keeps the parent invoice total in sync.
    """
    invoice = models.ForeignKey(
        Invoice,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name="Faktúra",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Názov položky",
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Množstvo",
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Cena za jednotku",
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        verbose_name="Suma",
    )

    def save(self, *args, **kwargs):
        """
        Calculate item total before saving and update parent invoice total.
        """
        self.total = (self.quantity or Decimal("0")) * (self.unit_price or Decimal("0"))
        super().save(*args, **kwargs)
        if self.invoice_id:
            self.invoice.recalculate_total()

    def delete(self, *args, **kwargs):
        """
        Recalculate parent invoice total after item removal.
        """
        invoice = self.invoice
        super().delete(*args, **kwargs)
        invoice.recalculate_total()

    def __str__(self):
        """
        Human-readable item label.
        """
        return self.name
