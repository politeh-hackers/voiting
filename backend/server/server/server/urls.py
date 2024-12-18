from django.urls import path, include

urlpatterns = [
    path('media/', include('media.urls')),
    path('actual/', include('actual.urls')),
    path('appeals/', include('appeals.urls')),
    path('category/', include('category.urls')),
    path('admin/', include('users.urls')),
]

