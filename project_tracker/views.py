import django_filters
from django.utils.safestring import mark_safe

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django_filters.filters import UUIDFilter
from rest_framework import generics
from rest_framework import filters
from rest_framework import pagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from . import jsonh

from .models import Organization, Project, Tag
from .serializers import OrganizationSerializer, ProjectSerializer, ProjectSerializerForList, \
    OrganizationSerializerForList


class ResultsPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page': self.page.number,
            'page_size': 100,
            'results': data
        })

class MultipleUUIDFilter(django_filters.MultipleChoiceFilter, django_filters.filters.UUIDFilter):
    def __init__(self, **kwargs):
        super(MultipleUUIDFilter, self).__init__(**kwargs)

class JsonListView(ListView):

    template_name = 'projecttracker/generic.json'
    content_type = "application/json"
    valid_formats = 'hjson','json','html'
    serializer = None

    def get_context_data(self, *args, **kwargs):
        response_format = self.kwargs.get('response_format')
        assert response_format in self.valid_formats
        if response_format == 'html':
            self.content_type = "text/html"
            self.template_name = 'projecttracker/generic.json.html'

        if response_format == 'hjson' or self.request.GET.get('hjson'):
            json = mark_safe(jsonh.dumps(self.serializer(self.queryset, many=True).data))
        else:
            json = mark_safe(JSONRenderer().render(self.serializer(self.queryset, many=True).data))

        return {'json': json}


class TagList(JsonListView):
    queryset = Tag.objects.all()


class ProjectList(JsonListView):
    """
    Return a list of projects; if a "modified-after" date is specified return only projects
    created or modified after a certain date
    """
    queryset = Project.objects.all().prefetch_related('tag', 'organization')
    serializer = ProjectSerializerForList


class OrganizationList(JsonListView):
    """
    Return a list of organizations; if a "modified-after" date is specified return only projects
    created or modified after a certain date
    """
    queryset = Organization.objects.all().prefetch_related('project_set')
    serializer = OrganizationSerializerForList



class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.MultipleChoiceFilter(choices=Project.PROJECT_STATUS_CHOICES)
    # tag = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())

    # Specific filtering for different groups
    activity = django_filters.ModelMultipleChoiceFilter(name='tag', queryset=Tag.objects.filter(group="Activity"))
    beneficiary = django_filters.ModelMultipleChoiceFilter(name='tag', queryset=Tag.objects.filter(group="Beneficiary"))
    sector = django_filters.ModelMultipleChoiceFilter(name='tag', queryset=Tag.objects.filter(group="Sector"))
    org_id = django_filters.ModelMultipleChoiceFilter(name='organization', queryset=Organization.objects.all())

    class Meta:
        model = Project
        fields = ['name','status', 'activity', 'org_id', 'status']


class OrganizationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.MultipleChoiceFilter(choices = Organization.ORGANIZATION_TYPE_CHOICES)
    active = django_filters.BooleanFilter()

    class Meta:
        model = Organization
        fields = ['name', 'type','active']



class HomePageView(TemplateView):

    template_name = "projecttracker/homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['PROJECT_STATUS_CHOICES'] = Project.PROJECT_STATUS_CHOICES
        context['filter'] = {
            'activity': Tag.objects.filter(group = 'Activity').values('description', 'id'),
            'sector': Tag.objects.filter(group = 'Sector').values('description', 'id'),
            'beneficiary': Tag.objects.filter(group = 'Beneficiary').values('description', 'id'),

        }

        return context


class OrganizationListAPI(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class=OrganizationFilter
    pagination_class=ResultsPagination

class ProjectListAPI(generics.ListAPIView):
    queryset = Project.objects.prefetch_related('tag','organization')
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class=ProjectFilter
    pagination_class=ResultsPagination


class ProjectDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Project.objects.all()
    queryset = Project.objects.prefetch_related('tag','organization')
    serializer_class = ProjectSerializer