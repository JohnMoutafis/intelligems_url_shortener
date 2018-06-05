from django.contrib import admin

from intelligems.url_shortener.models import AvailableUrls, ShortenedUrls


@admin.register(AvailableUrls)
class AvailableUrlsAdmin(admin.ModelAdmin):
    pass


@admin.register(ShortenedUrls)
class ShortenedUrlsAdmin(admin.ModelAdmin):
    pass
