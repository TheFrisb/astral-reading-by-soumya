from django.db import models

# Create your models here.
class InternalBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True