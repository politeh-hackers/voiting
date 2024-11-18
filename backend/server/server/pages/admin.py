from django.contrib import admin
from .models import Media, Actual, Appeal, Category, MediaTag, ActualTag

admin.site.register(Media)
admin.site.register(Actual)
admin.site.register(Category)
admin.site.register(Appeal)
admin.site.register(MediaTag)
admin.site.register(ActualTag)