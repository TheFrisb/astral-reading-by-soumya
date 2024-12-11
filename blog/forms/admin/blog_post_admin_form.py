from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from blog.models import BlogPost, Category


class BlogPostAdminForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=FilteredSelectMultiple(verbose_name="Tags", is_stacked=False),
        label="",
    )

    class Meta:
        model = BlogPost
        fields = "__all__"
