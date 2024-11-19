from django.contrib import admin

from blog.forms.admin.blog_post_admin_form import BlogPostAdminForm
from core.admin import InternalBaseAdmin
from .models import BlogPost


# Create your models here.


# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(InternalBaseAdmin):
    form = BlogPostAdminForm
