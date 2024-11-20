from django.http import Http404
from django.views.generic import DetailView, TemplateView

from .mixins import PageTagsMixin
from .services.horoscopes_service import HoroscopeService


class HomeView(PageTagsMixin, TemplateView):
    template_name = "core/pages/horoscopes.html"
    page_title = "Home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horoscope_service = HoroscopeService()
        context["horoscope_signs"] = horoscope_service.get_horoscope_signs(
            get_weekly_horoscope=True, get_monthly_horoscope=True
        )
        return context


class HoroscopeDetailView(PageTagsMixin, DetailView):
    template_name = "core/pages/horoscope_detail.html"
    context_object_name = "horoscope_sign"

    def get_object(self):
        """
        Retrieves the horoscope sign based on the 'sign_name' URL parameter.
        """
        sign_name = self.kwargs.get("sign_name")
        horoscope_service = HoroscopeService()
        horoscope_signs = horoscope_service.get_horoscope_signs(
            get_weekly_horoscope=True, get_monthly_horoscope=True
        )

        # Find the horoscope sign by name
        horoscope_sign = horoscope_signs.get(name=sign_name)
        if not horoscope_sign:
            raise Http404("Horoscope sign not found")
        return horoscope_sign

    def get_page_title(self):
        """
        Generates a dynamic page title based on the horoscope sign's name.
        """
        horoscope_sign = self.get_object()
        return f"{horoscope_sign.name} Horoscope"
