class PageTagsMixin:
    """
    Mixin to add page tags to the context.
    """

    page_title = None  # Should be set in subclasses

    def get_page_title(self):
        """
        Returns the page title. Subclasses can override this method
        if they need dynamic titles.
        """
        return self.page_title

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
        return context
