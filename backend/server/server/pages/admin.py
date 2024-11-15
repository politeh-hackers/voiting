from django.contrib import admin
from .models import Media, Actual, Appeal, Category

admin.site.register(Media)
admin.site.register(Actual)
admin.site.register(Category)
admin.site.register(Appeal)
