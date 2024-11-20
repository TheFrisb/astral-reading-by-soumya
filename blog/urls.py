from django.urls import path

from blog.views import BlogHomeView, BlogDetailView

app_name = "blog"
urlpatterns = [
    path("", BlogHomeView.as_view(), name="home"),
    path("<str:slug>/", BlogDetailView.as_view(), name="blog_post_detail"),
]
