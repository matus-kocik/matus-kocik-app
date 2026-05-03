from django.db import models
from tinymce.models import HTMLField

from common.models import PublishableModel, SlugModel, TimeStampedModel


class Post(TimeStampedModel, SlugModel, PublishableModel):
    title = models.CharField(max_length=200)
    content = HTMLField()
    image = models.ImageField(upload_to="blog/", blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Článok"
        verbose_name_plural = "Články"

    def __str__(self):
        return self.title
