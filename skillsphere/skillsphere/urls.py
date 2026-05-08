from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from .views import health, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health, name='health'),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),
    path('interviews/', include('interviews.urls')),
    path('skills/', include('skills.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif settings.SERVE_MEDIA:
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
