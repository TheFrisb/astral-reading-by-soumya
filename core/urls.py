from django.urls import path

from .views import HomeView, HoroscopeDetailView

app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "horoscope/<str:sign_name>/",
        HoroscopeDetailView.as_view(),
        name="horoscope_detail",
    ),
]
