from django.views.generic import DetailView, ListView

from blog.models import BlogPost
from blog.services.BlogService import BlogService
from core.mixins import PageTagsMixin
from core.services.horoscopes_service import HoroscopeService


# Create your views here.
class BlogHomeView(ListView, PageTagsMixin):
    template_name = "blog/pages/home.html"
    page_title = "Home"
    model = BlogPost
    context_object_name = "blog_posts"
    paginate_by = 10  # Number of posts per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horoscope_service = HoroscopeService()
        context["horoscope_signs"] = horoscope_service.get_horoscope_signs()
        return context

    def get_queryset(self):
        blog_service = BlogService()
        return blog_service.get_blog_posts()


class BlogDetailView(DetailView, PageTagsMixin):
    template_name = "blog/pages/detail.html"
    page_title = "Blog Post Detail"
    model = BlogPost
    context_object_name = "blog_post"

    def get_queryset(self):
        return BlogPost.objects.filter(slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_service = BlogService()
        context["related_blog_posts"] = blog_service.get_related_by_post(self.object)
        return context
