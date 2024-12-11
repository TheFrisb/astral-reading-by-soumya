class PageTagsMixin:
    """
    Mixin to add page tags to the context.
    """

    def get_page_title(self):
        """
        Returns the page title. Subclasses can override this method
        if they need dynamic titles.
        """
        if hasattr(super(), "get_page_title"):
            return super().get_page_title()

        if hasattr(self, "page_title"):
            return self.page_title

        return "Astral Readings by Soumya"
 
    def get_page_tags(self):
        """
        Generates the page tags using the page title.
        """
        return {
            "title": self.get_page_title(),
        }

    def get_context_data(self, **kwargs):
        """
        Adds 'page_tags' to the context.
        """
        context = super().get_context_data(**kwargs)
        context["page_tags"] = self.get_page_tags()
        context["testimonial_star_range"] = range(1, 6)
        return context
