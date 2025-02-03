from django.contrib.sitemaps import Sitemap
from actual.models import Actual
from appeals.models import Appeal
from biography.models import Biography
from media.models import Media
from django.contrib.sites.models import Site


class ActualSitemap(Sitemap):
    protocol = 'http'
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Actual.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/actual/{Actual.slug}/"   

    # def get_domain(self):  
    #     return Site.objects.get_current().domain

class AppealsSitemap(Sitemap):
    protocol = 'http'
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Appeal.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/appeals/{Appeal.slug}/"   

class BiographySitemap(Sitemap):
    protocol = 'http'
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Biography.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/biography/{Biography.slug}/" 

class MediaSitemap(Sitemap):
    protocol = 'http'
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Media.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/media/{Media.slug}/" 

sitemaps = {
    "actual": ActualSitemap(),
    "appeals": AppealsSitemap(),
    "biography": BiographySitemap(),
    "media": MediaSitemap(),
}
