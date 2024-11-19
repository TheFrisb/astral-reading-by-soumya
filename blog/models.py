from django.db import models

from core.models import InternalBaseModel, Horoscope


class BlogPost(InternalBaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    horoscopes = models.ManyToManyField(
        "core.HoroscopeSign", blank=True, related_name="blog_posts"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
