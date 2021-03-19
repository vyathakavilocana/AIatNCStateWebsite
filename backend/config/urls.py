from django.urls import path
from django.contrib import admin
from django.contrib.auth import logout
from django.conf.urls import include
from config.api import api


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('logout/', logout, {'next_page': '/'}, name='logout'),
    path('api/', include(api.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('sentry-debug/', trigger_error),
]
