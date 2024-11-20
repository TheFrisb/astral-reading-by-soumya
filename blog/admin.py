from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.db import models
from django.forms import TextInput

from blog.forms.admin.blog_post_admin_form import BlogPostAdminForm
from core.admin import InternalBaseAdmin
from .models import BlogPost, Category


# Create your models here.


# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(InternalBaseAdmin):
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "100"})},
    }
    form = BlogPostAdminForm
    readonly_fields = ("slug",)
    list_display = ("title", "tags", "created_at")

    list_filter = ("categories",)

    def tags(self, obj):
        return ", ".join([tag.name for tag in obj.categories.all()])

    class Media:
        css = {"all": ("css/admin/custom_admin.css",)}


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, InternalBaseAdmin):
    list_display = ("name", "sortable_order")
    readonly_fields = ("slug",)

    ordering = ("sortable_order",)
    search_fields = ("name",)
