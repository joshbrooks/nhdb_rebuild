from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    url(r'^api/organization/$', views.OrganizationListAPI.as_view(), name='api-organization-list'),
    url(r'^api/project/$', views.ProjectListAPI.as_view()),
    url(r'^api/project/(?P<pk>[^/]+)/$', views.ProjectDetailAPI.as_view()),

    url(r'projects.(?P<response_format>[^/]+)', cache_page(60 * 5)(views.ProjectList.as_view())),
    url(r'organization.(?P<response_format>[^/]+)', cache_page(60 * 5)(views.OrganizationList.as_view())),
    # url(r'tags.(?P<response_format>[^/]+)', cache_page(60 * 5)(views.TagList.as_view())),

    url(r'projects', views.ProjectList.as_view()),

    ]