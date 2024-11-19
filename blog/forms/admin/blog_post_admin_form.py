from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from blog.models import BlogPost
from core.models import HoroscopeSign


class BlogPostAdminForm(forms.ModelForm):
    horoscopes = forms.ModelMultipleChoiceField(
        queryset=HoroscopeSign.objects.all(),
        widget=FilteredSelectMultiple(verbose_name="Horoscope Signs", is_stacked=False),
    )

    class Meta:
        model = BlogPost
        fields = "__all__"
