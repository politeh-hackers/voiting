from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', include('new_admin.urls')),
    path('', include('pages.urls'))
]
