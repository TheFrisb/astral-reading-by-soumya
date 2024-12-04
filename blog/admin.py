from django.contrib import admin
from django.db import models
from django.forms import TextInput

from blog.forms.admin.blog_post_admin_form import BlogPostAdminForm
from core.admin import InternalBaseAdmin
from .models import BlogPost


# Create your models here.


# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(InternalBaseAdmin):
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "100"})},
    }
    form = BlogPostAdminForm
    readonly_fields = ("slug",)
