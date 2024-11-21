from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #path('admin/', include('adm.urls')),
    path('', include('pages.urls')),

]

