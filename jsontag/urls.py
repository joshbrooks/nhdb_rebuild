from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [

    url(r'^translations.json$', cache_page(60 * 5)(views.TranslationList.as_view()), name='translations'),

    ]

