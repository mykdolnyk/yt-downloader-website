from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from videos import views as video_views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', video_views.index_page, name='index_page'),
    path('video/', video_views.video_page, name='video_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
