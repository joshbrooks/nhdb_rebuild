import django_filters
from django.http import HttpResponse, Http404
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.decorators.gzip import gzip_page
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from rest_framework import filters
from rest_framework import generics
from rest_framework import pagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from jsontag.models import Tag
from . import jsonh
from . import serializers
from .models import Organization, Project, Person


def gz(content):
    from io import BytesIO, StringIO
    import gzip
    if not isinstance(content, bytes):
        content = content.encode()
    zbuf = BytesIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(content)
    zfile.close()
    compressed_content = zbuf.getvalue()
    return compressed_content

class JSONHRenderer(JSONRenderer):
    """
    A renderer which returns the more compact HJson format
    """

    def render(self, data, indent=1, separators=None):
        return jsonh.dumps(
            data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
        )


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, compress=False, media_type="application/json; indent=4", **kwargs):

        self.headers = {}
        content = JSONRenderer().render(data, accepted_media_type=media_type)
        if compress:
            content = gz(content)
        kwargs['content_type'] = 'application/json'

        super(JSONResponse, self).__init__(content, **kwargs)

        if compress:
            self['Content-Encoding'] = 'gzip'
            self['Content-Length'] = str(len(content))


class JSONHResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, compress=False, **kwargs):
        content = JSONHRenderer().render(data, indent=1)
        if compress:
            content = gz(content)
        kwargs['content_type'] = 'application/json'
        super(JSONHResponse, self).__init__(content, **kwargs)

        if compress:
            self['Content-Encoding'] = 'gzip'
            self['Content-Length'] = str(len(content))

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

    valid_formats = 'jsonh','json','html', 'htmlh'
    serializer = None

    @property
    def ser_data(self):
        return self.serializer(self.queryset, many=True).data

    def get_context_data(self, *args, **kwargs):
        response_format = self.kwargs.get('response_format')
        if response_format == 'html':
            return {'json': mark_safe(JSONRenderer().render(self.ser_data).decode())}
        if response_format == 'htmlh':
            return {'json': mark_safe(JSONHRenderer().render(self.ser_data))}
        else:
            return self.ser_data

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        response_format = self.kwargs.get('response_format')

        if response_format == 'html':
            return TemplateResponse(request, 'projecttracker/generic.json.html', context=context )
        elif response_format == 'htmlh':
            return TemplateResponse(request, 'projecttracker/generic.jsonh.html', context=context)
        elif response_format == 'jsonh':
            return JSONHResponse(context, compress=True)
        elif response_format == 'json':
            response = JSONResponse(context, compress=True)

            return response
        else:
            raise AssertionError('Unhandled response type')


class ProjectList(JsonListView):
    """
    Return a list of projects; if a "modified-after" date is specified return only projects
    created or modified after a certain date
    """
    queryset = Project.objects.all().prefetch_related('tag', 'organization', 'projectperson_set', 'person')
    serializer = serializers.ProjectSerializer


class OrganizationList(JsonListView):
    """
    Return a list of organizations; if a "modified-after" date is specified return only projects
    created or modified after a certain date
    """
    queryset = Organization.objects.all().prefetch_related('project_set')
    serializer = serializers.OrganizationSerializer


class PersonList(JsonListView):

    queryset = Person.objects.all().prefetch_related('project_set').prefetch_related('organization')
    serializer = serializers.PersonSerializer


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.MultipleChoiceFilter(choices=Project.PROJECT_STATUS_CHOICES)
    # tag = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())

    # Specific filtering for different groups
    activity = django_filters.ModelMultipleChoiceFilter(name='tag', queryset=Tag.objects.filter(group="ACT"))
    beneficiary = django_filters.ModelMultipleChoiceFilter(name='tag', queryset=Tag.objects.filter(group="BEN"))
    sector = django_filters.ModelMultipleChoiceFilter(name='tag', queryset=Tag.objects.filter(group="INV"))
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
            'activity': Tag.objects.filter(group = 'ACT'),
            'sector': Tag.objects.filter(group = 'INV'),
            'beneficiary': Tag.objects.filter(group = 'BEN'),

        }

        return context


class OrganizationListAPI(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class=OrganizationFilter
    pagination_class=ResultsPagination

class ProjectListAPI(generics.ListAPIView):
    queryset = Project.objects.prefetch_related('tag','organization')
    serializer_class = serializers.ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class=ProjectFilter
    pagination_class=ResultsPagination


class ProjectDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Project.objects.all()
    queryset = Project.objects.prefetch_related('tag','organization')
    serializer_class = serializers.ProjectSerializer