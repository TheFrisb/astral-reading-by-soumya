from django.db.models import QuerySet

from blog.models import BlogPost, Category
from core.models import Horoscope


class BlogService:
    def get_blog_post_by_slug(self, slug) -> BlogPost | None:
        try:
            return BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            return None

    def get_related_by_post(self, blog_post: BlogPost) -> QuerySet:
        tags = blog_post.categories.all()

        return (
            BlogPost.objects.filter(categories__in=tags)
            .exclude(id=blog_post.id)
            .order_by("-id")[:6]
        )

    def get_related_by_horoscope_sign(self, horoscope_sign: Horoscope) -> QuerySet:
        category = Category.objects.filter(name=horoscope_sign.name).first()

        if not category:
            return BlogPost.objects.none()

        return BlogPost.objects.filter(categories=category).order_by("-id")[:6]

    def get_category_by_slug(self, param):
        return Category.objects.get(slug=param)
