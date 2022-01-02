from django.contrib import admin
from .models import URL

class URLAdmin(admin.ModelAdmin):
    list_display = [field.name for field in URL._meta.get_fields() if field.auto_created is False]


admin.site.register(URL, URLAdmin)
