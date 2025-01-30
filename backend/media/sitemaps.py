from django.contrib.sitemaps import Sitemap
from .models import Media

class MediaSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Media.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
