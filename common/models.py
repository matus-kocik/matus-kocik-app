from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides created and updated timestamps.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Vytvorené",
        help_text="Dátum a čas vytvorenia záznamu",
        db_index=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Aktualizované",
        help_text="Dátum a čas poslednej úpravy",
    )

    class Meta:
        abstract = True


class SlugModel(models.Model):
    """
    Abstract model that provides an auto-generated unique slug field.
    """
    slug = models.SlugField(
        unique=True,
        blank=True,
        db_index=True,
        verbose_name="Slug",
        help_text="URL identifikátor (automaticky generovaný, ak nie je vyplnený)",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            source = None

            if hasattr(self, "title") and self.title:
                source = self.title
            elif hasattr(self, "latin_name") and self.latin_name:
                source = self.latin_name
            elif hasattr(self, "name") and self.name:
                source = self.name

            if source and str(source).strip():
                base_slug = slugify(source)
                slug = base_slug
                counter = 1

                ModelClass = self.__class__
                while ModelClass.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                self.slug = slug

        super().save(*args, **kwargs)


class SEOModel(models.Model):
    """
    Abstract model providing basic SEO metadata fields.
    """
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Meta titulok",
        help_text="Titulok pre SEO (HTML <title>)",
    )
    meta_description = models.TextField(
        blank=True,
        verbose_name="Meta popis",
        help_text="Krátky popis pre vyhľadávače",
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Meta kľúčové slová",
        help_text="Kľúčové slová oddelené čiarkou",
    )

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    """
    Abstract model implementing soft delete functionality.
    """
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="Zmazané",
        help_text="Označuje záznam ako soft zmazaný",
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Zmazané dňa",
        help_text="Dátum a čas soft zmazania",
    )

    class Meta:
        abstract = True

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, hard=False, *args, **kwargs):
        if hard:
            super().delete(*args, **kwargs)
        else:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save()


class PublishableModel(models.Model):
    """
    Abstract model handling publication state and timestamps.
    """
    is_published = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Publikované",
        help_text="Určuje, či je záznam verejne viditeľný",
    )
    published_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Publikované dňa",
        help_text="Dátum a čas publikovania",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
