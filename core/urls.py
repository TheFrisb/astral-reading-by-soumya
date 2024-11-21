from django.urls import path

from .views import HomeView, HoroscopeDetailView, FrequentlyAskedQuestionsView

app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "horoscope/<str:sign_name>/",
        HoroscopeDetailView.as_view(),
        name="horoscope_detail",
    ),
    path("frequently-asked-questions/", FrequentlyAskedQuestionsView.as_view(), name="faq"),
]
