from django.urls import path

from .views import (
    HomeView,
    HoroscopeDetailView,
    FrequentlyAskedQuestionsView,
    ReadingsView,
    AboutView,
    CheckoutView,
    stripe_webhook,
    ThankYouView,
    HoroscopeListView,
    LocationSearchView,
    LeaveReviewView,
)

app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("horoscopes/", HoroscopeListView.as_view(), name="horoscope_list"),
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
    path("checkout/<uuid:reading_id>/", CheckoutView.as_view(), name="checkout"),
    path("thank-you/<uuid:order_id>/", ThankYouView.as_view(), name="thank_you"),
    path("stripe/webhook/", stripe_webhook, name="stripe_webhook"),
    path("location-search/", LocationSearchView.as_view(), name="location_search"),
    path(
        "leave-review/<uuid:order_id>/",
        LeaveReviewView.as_view(),
        name="leave_review",
    ),
]
