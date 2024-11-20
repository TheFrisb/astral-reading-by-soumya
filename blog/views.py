from django.views.generic import DetailView, ListView

from blog.models import BlogPost, Category
from blog.services.BlogService import BlogService
from core.mixins import PageTagsMixin
from core.services.horoscopes_service import HoroscopeService


# Create your views here.
class BlogHomeView(ListView, PageTagsMixin):
    template_name = "blog/pages/home.html"
    page_title = "Blog"
    model = BlogPost
    context_object_name = "blog_posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horoscope_service = HoroscopeService()
        context["horoscope_signs"] = horoscope_service.get_horoscope_signs()
        context["category_filter"] = self.get_category_filter()
        context["categories"] = Category.objects.all().order_by("sortable_order")
        return context

    def get_queryset(self):
        categoryFilter = self.get_category_filter()

        if categoryFilter:
            return BlogPost.objects.filter(categories__slug=categoryFilter).order_by(
                "-id"
            )

        return BlogPost.objects.all().order_by("-id")

    def get_category_filter(self):
        return self.request.GET.get("filter", None)


class BlogDetailView(PageTagsMixin, DetailView):
    template_name = "blog/pages/detail.html"
    page_title = "Blog Post Detail"
    model = BlogPost
    context_object_name = "blog_post"

    def get_queryset(self):
        return BlogPost.objects.filter(slug=self.kwargs["slug"])  # Return a QuerySet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_service = BlogService()
        context["related_blog_posts"] = blog_service.get_related_by_post(self.object)
        return context

    def get_page_title(self):
        return self.object.title
