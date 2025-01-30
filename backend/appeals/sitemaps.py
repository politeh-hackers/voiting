from django.contrib.sitemaps import Sitemap
from .models import Appeal

class AppealsSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return Appeal.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
