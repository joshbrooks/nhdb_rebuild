"""nhdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from nhdb import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^nhdb/', include('project_tracker.urls', namespace='nhdb')),
    url(r'^jt/', include('jsontag.urls', namespace='jsontag')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
# TODO
# Not yet compatible with 1.10
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]