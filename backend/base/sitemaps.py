from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from actual.models import Actual
from appeals.models import Appeal
from biography.models import Biography
from media.models import Media

# Sitemap для Actual
class ActualSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Actual.objects.all()

    def location(self, obj):
        return reverse('actual_detail', args=[obj.id])  # Указание URL для каждого объекта

    def lastmod(self, obj):
        return obj.updated_at

# Sitemap для Appeals
class AppealsSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Appeal.objects.all()

    def location(self, obj):
        return reverse('appeal_detail', args=[obj.id])  # Указание URL для каждого объекта

    def lastmod(self, obj):
        return obj.updated_at

# Sitemap для Biography
class BiographySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Biography.objects.all()

    def location(self, obj):
        return reverse('biography_detail', args=[obj.id])  # Указание URL для каждого объекта

    def lastmod(self, obj):
        return obj.updated_at

# Sitemap для Media
class MediaSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Media.objects.all()

    def location(self, obj):
        return reverse('media_detail', args=[obj.id])  # Указание URL для каждого объекта

    def lastmod(self, obj):
        return obj.updated_at


# Объединяем все Sitemap в один словарь
sitemaps = {
    "actual": ActualSitemap(),
    "appeals": AppealsSitemap(),
    "biography": BiographySitemap(),
    "media": MediaSitemap(),
}
