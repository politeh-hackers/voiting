from django.contrib.sitemaps import Sitemap
from .models import Biography

class BiographySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Biography.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
