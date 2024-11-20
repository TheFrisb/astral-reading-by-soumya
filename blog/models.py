from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from core.models import InternalBaseModel


class Category(InternalBaseModel):
    image = models.ImageField(upload_to="blog_category_images", blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    sortable_order = models.IntegerField(default=0, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            unique_slug = self.slug
            num = 1
            while (
                Category.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists()
            ):
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('blog:home')}?filter={self.slug}"

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class BlogPost(InternalBaseModel):
    image = models.ImageField(upload_to="blog_images")
    title = models.CharField(max_length=100)
    content = CKEditor5Field("Content")
    categories = models.ManyToManyField(
        Category, related_name="blog_posts", verbose_name="Tags"
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

    @property
    def get_preview(self):
        plain_text = strip_tags(self.content)  # Remove HTML tags
        words = plain_text.split()[:20]  # Get the first 20 words
        return " ".join(words)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
