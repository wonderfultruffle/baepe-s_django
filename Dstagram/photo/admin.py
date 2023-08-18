from django.contrib import admin
from .models import Photo
# Register your models here.

class PhtoAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "created", "updated"]
    raw_id_fields = ["author"]
    search_filter = ["text", "created"]
    list_filter = ["created", "updated", "author"]
    ordering = ["-updated", "-created"]

admin.site.register(Photo, PhtoAdmin)