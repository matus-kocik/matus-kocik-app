from django.core.exceptions import ValidationError
from django.db import models

from common.models import PublishableModel, SlugModel, TimeStampedModel


class Node(
    TimeStampedModel,
    SlugModel,
    PublishableModel,
):
    """
    A node in the economics family tree.

    A node can represent a person, economic school, theory,
    concept, work, event, or another relevant element
    of economic thought.
    """

    class NodeType(models.TextChoices):
        PERSON = "person", "Osobnosť"
        SCHOOL = "school", "Ekonomická škola"
        THEORY = "theory", "Teória / smer"
        CONCEPT = "concept", "Pojem / koncept"
        WORK = "work", "Dielo"
        EVENT = "event", "Udalosť"

    name = models.CharField(
        max_length=200,
        verbose_name="Názov",
        help_text="Názov uzla, napr. Adam Smith alebo Klasická ekonómia",
    )

    node_type = models.CharField(
        max_length=20,
        choices=NodeType.choices,
        db_index=True,
        verbose_name="Typ",
        help_text="Typ prvku v rodokmeni ekonómie",
    )

    year_from = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Rok od",
        help_text="Začiatočný rok alebo rok vzniku",
    )

    year_to = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Rok do",
        help_text="Koncový rok, ak je relevantný",
    )

    period_label = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Obdobie",
        help_text=(
            "Voliteľné slovné obdobie, napr. 18. storočie, "
            "koniec 19. storočia alebo od 1930"
        ),
    )

    short_description = models.TextField(
        blank=True,
        verbose_name="Krátky popis",
        help_text="Stručný popis vhodný pre graf a časovú os",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Detailný popis",
        help_text="Podrobnejšie informácie zobrazované v detaile uzla",
    )

    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="Poradie",
        help_text="Manuálne poradie pri zobrazovaní uzlov",
    )

    editor_note = models.TextField(
        blank=True,
        verbose_name="Poznámka redaktora",
    )

    class Meta:
        ordering = ["order", "year_from", "name"]
        verbose_name = "Uzol"
        verbose_name_plural = "Uzly"

    def __str__(self):
        return self.name


class Connection(
    TimeStampedModel,
    PublishableModel,
):
    """
    A directed relationship between two nodes in the economics family tree.
    """

    class ConnectionType(models.TextChoices):
        INFLUENCED = "influenced", "Ovplyvnil"
        REPRESENTS = "represents", "Predstaviteľ"
        FOUNDED = "founded", "Zakladateľ"
        DEVELOPED = "developed", "Rozvinul"
        AUTHOR = "author", "Autor"
        REACTED_TO = "reacted_to", "Reakcia na"
        OPPOSED = "opposed", "Vymedzil sa voči"
        CRITICIZED = "criticized", "Kritizoval"
        RELATED = "related", "Súvisí s"
        BELONGS_TO = "belongs_to", "Patrí do"
        FOLLOWED = "followed", "Nadviazal na"

    source = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="outgoing_connections",
        verbose_name="Zdroj",
        help_text="Uzol, z ktorého vzťah vychádza",
    )

    target = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="incoming_connections",
        verbose_name="Cieľ",
        help_text="Uzol, do ktorého vzťah smeruje",
    )

    connection_type = models.CharField(
        max_length=20,
        choices=ConnectionType.choices,
        db_index=True,
        verbose_name="Typ prepojenia",
        help_text="Význam vzťahu medzi uzlami",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Popis",
        help_text="Voliteľné vysvetlenie vzťahu medzi uzlami",
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Poradie",
        help_text="Manuálne poradie prepojenia",
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Prepojenie"
        verbose_name_plural = "Prepojenia"
        constraints = [
            models.UniqueConstraint(
                fields=["source", "target", "connection_type"],
                name="unique_rodokmen_connection",
            ),
        ]

    def clean(self):
        super().clean()

        if self.source_id and self.source_id == self.target_id:
            raise ValidationError(
                {"target": "Uzol nemôže byť prepojený sám so sebou."},
            )

    def __str__(self):
        return (
            f"{self.source} → "
            f"{self.get_connection_type_display()} → "
            f"{self.target}"
        )
