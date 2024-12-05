from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from core.models import InternalBaseModel


class BlogPost(InternalBaseModel):
    title = models.CharField(max_length=100)
    content = CKEditor5Field("Content", config_name="default")
    horoscopes = models.ManyToManyField(
        "core.HoroscopeSign", blank=True, related_name="blog_posts"
    )

    slug = models.SlugField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            unique_slug = self.slug
            num = 1
            while (
                BlogPost.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists()
            ):
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:blog_post_detail", args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
