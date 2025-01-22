from django.urls import reverse_lazy


class PageTagsMixin:
    """
    Mixin to add page tags to the context and require login.
    """

    login_url = "/admin/login/"

    def get_login_url(self):
        # Force a redirect to core:home after login by passing 'next' parameter
        return f"{super().get_login_url()}?next={reverse_lazy('core:home')}"

    def get_page_title(self):
        if hasattr(super(), "get_page_title"):
            return super().get_page_title()

        if hasattr(self, "page_title"):
            return self.page_title

        return "Astral Reading by Soumya"

    def get_page_tags(self):
        return {
            "title": self.get_page_title(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_tags"] = self.get_page_tags()
        context["testimonial_star_range"] = range(1, 6)
        return context
