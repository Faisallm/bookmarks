from django.contrib import admin
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "image", "created"]
    list_filter = ["created"]
    raw_id_fields = ["user"]

admin.site.register(Image, ImageAdmin)
