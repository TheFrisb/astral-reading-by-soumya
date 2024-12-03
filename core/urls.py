from django.urls import path

from .views import (
    HomeView,
    HoroscopeDetailView,
    FrequentlyAskedQuestionsView,
    ReadingsView,
    AboutView,
)

app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "horoscope/<str:sign_name>/",
        HoroscopeDetailView.as_view(),
        name="horoscope_detail",
    ),
    path(
        "frequently-asked-questions/",
        FrequentlyAskedQuestionsView.as_view(),
        name="faq",
    ),
    path("readings/", ReadingsView.as_view(), name="readings"),
    path("about/", AboutView.as_view(), name="about"),
]
