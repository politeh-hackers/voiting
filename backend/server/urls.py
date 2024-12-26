from django.urls import path, include
from media.views import ImageView
from actual.views import ImageView

urlpatterns = [
    path('media/', include('media.urls')),
    path('actual/', include('actual.urls')),
    path('appeals/', include('appeals.urls')),
    path('category/', include('category.urls')),
    path('admin/', include('users.urls')),
    path('admin/image', ImageView.as_view()),
    path('admin/image/<str:file_name>', ImageView.as_view()),

]
