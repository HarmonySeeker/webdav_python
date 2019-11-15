"""Link router file."""

from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^source/(?P<path>[a-zA-Z\/]*)', views.source, name='init_app-source'),
    path('full_source/', views.full_source, name='init_app-full_source'),
    path('upload/', views.file_upload, name='init-app_file_upload'),
    #    path('list', views.list, name='init_app-list'),
    #    url(r'^list_all/(?P<path>[a-zA-Z\/]*)', views.list_all, name='init_app-list_all'),
#    path('delete_dir', views.delete_dir, name='delete_dir'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
