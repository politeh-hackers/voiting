from django.urls import path, include
from media.views import ImageView
from actual.views import ImageView
from base.sitemaps import sitemaps
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import index, sitemap

urlpatterns = [
    path('', include('mainpage.urls')),
    path('media/', include('media.urls')),
    path('biography/', include('biography.urls')),
    path('actual/', include('actual.urls')),
    path('appeals/', include('appeals.urls')),
    path('category/', include('category.urls')),
    path('biography/', include('biography.urls')),
    path('admin/', include('users.urls')),
    path('admin/image', ImageView.as_view()),
    path('admin/image/<str:file_name>', ImageView.as_view()),
    path('sitemap.xml', index, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
