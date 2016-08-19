from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    url(r'^$', views.Main.as_view(), name='nhdb'),
    url(r'^api/organization/$', views.OrganizationListAPI.as_view(), name='api-organization-list'),
    url(r'^api/project/$', views.ProjectListAPI.as_view(), name='project_list'),
    url(r'^api/project/(?P<pk>[^/]+)/$', views.ProjectDetailAPI.as_view(), name='project_detail'),

    url(r'^project.(?P<response_format>[^/]+)$', cache_page(60 * 5)(views.ProjectList.as_view()), name='project_data'),
    url(r'^organization.(?P<response_format>[^/]+)$', cache_page(60 * 5)(views.OrganizationList.as_view()), name='organization_data'),
    url(r'^person.(?P<response_format>[^/]+)$', cache_page(60 * 5)(views.PersonList.as_view()), name='person_data'),

    #
    # url(r'^project.(?P<response_format>[^/]+)$', views.ProjectList.as_view(), name='project_data'),
    # url(r'^organization.(?P<response_format>[^/]+)$', views.OrganizationList.as_view(), name='organization_data'),
    # url(r'^person.(?P<response_format>[^/]+)$', views.PersonList.as_view(), name='person_data'),
    #



    # url(r'tags.(?P<response_format>[^/]+)', cache_page(60 * 5)(views.TagList.as_view())),

    url(r'^projects', views.ProjectList.as_view()),

    ]

