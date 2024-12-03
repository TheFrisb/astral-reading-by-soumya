from django.db.models import QuerySet

from blog.models import BlogPost
from core.models import Horoscope


class BlogService:
    def get_blog_posts(self) -> QuerySet:
        return BlogPost.objects.all().order_by("-id")

    def get_blog_post_by_slug(self, slug) -> BlogPost | None:
        try:
            return BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            return None

    def get_related_by_post(self, blog_post: BlogPost) -> QuerySet:
        tags = blog_post.horoscopes.all()

        return BlogPost.objects.filter(horoscopes__in=tags).exclude(id=blog_post.id)[:6]

    def get_related_by_horoscope_sign(self, horoscope_sign: Horoscope) -> QuerySet:
        return BlogPost.objects.filter(horoscopes=horoscope_sign).order_by("-id")[:6]
