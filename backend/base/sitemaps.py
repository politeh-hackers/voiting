from django.contrib.sitemaps import Sitemap
from actual.models import Actual
from appeals.models import Appeal
from biography.models import Biography
from media.models import Media

class ActualSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Actual.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/actual/{obj.slug}/"  # Протокол и домен

class AppealsSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Appeal.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/appeals/{obj.slug}/"  # Протокол и домен

class BiographySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Biography.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/biography/{obj.slug}/"  # Протокол и домен

class MediaSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Media.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/media/{obj.slug}/"  # Протокол и домен

sitemaps = {
    "actual": ActualSitemap(),
    "appeals": AppealsSitemap(),
    "biography": BiographySitemap(),
    "media": MediaSitemap(),
}
