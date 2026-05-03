from django.conf import settings
from django.db import models


class Entity(models.Model):
    """
    Reusable business entity.
    Can act as supplier or customer.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entities",
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Názov subjektu",
    )
    ico = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="IČO",
    )
    dic = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="DIČ",
    )
    ic_dph = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="IČ DPH",
    )

    street = models.CharField(
        max_length=255,
        verbose_name="Ulica a číslo",
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Mesto",
    )
    zip_code = models.CharField(
        max_length=10,
        verbose_name="PSČ",
    )
    country = models.CharField(
        max_length=100,
        default="Slovensko",
        verbose_name="Krajina",
    )

    email = models.EmailField(
        blank=True,
        verbose_name="Email",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subjekt"
        verbose_name_plural = "Subjekty"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def default_bank_account(self):
        """
        Returns the default bank account for this entity.
        Falls back to the first available account if no default is set.
        Used by invoices, PDF rendering, and admin display.
        """
        return (
            self.bank_accounts.filter(is_default=True).first()
            or self.bank_accounts.first()
        )


class BankAccount(models.Model):
    """
    Bank account linked to an entity.
    """

    entity = models.ForeignKey(
        Entity,
        related_name="bank_accounts",
        on_delete=models.CASCADE,
        verbose_name="Subjekt",
    )
    iban = models.CharField(
        max_length=34,
        verbose_name="IBAN",
    )
    swift = models.CharField(
        max_length=11,
        blank=True,
        verbose_name="SWIFT / BIC",
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name="Predvolený účet",
    )

    class Meta:
        verbose_name = "Bankový účet"
        verbose_name_plural = "Bankové účty"
        ordering = ["-is_default"]

    def __str__(self):
        return f"{self.iban}"

    def save(self, *args, **kwargs):
        if self.is_default:
            BankAccount.objects.filter(entity=self.entity, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
