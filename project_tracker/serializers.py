import uuid

from rest_framework import serializers
import calendar
from django.utils import six
from rest_framework.fields import Field, UUIDField

from projecttracker.uuidencode import uuid_to_base64, base64_to_uuid
from .models import Organization, OrganizationPlace, Tag, Project, ProjectPlace


class Base64UUIDField(Field):

    def to_internal_value(self, data):
        return base64_to_uuid(data)

    def to_representation(self, value):
        return uuid_to_base64(value)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'acronym', 'description', 'active', 'fulltimestaff', 'parttimestaff', 'verified' ,'id', 'phone' ,'phone_other', 'email', 'fax', 'facebook')


class TagSerializer(serializers.ModelSerializer):
    id = Base64UUIDField()
    class Meta:
        model = Tag
        # queryset = Tag.objects.filter(group='Sector')
        fields = ('description', 'group')


class OrganizationRelationSerializer(serializers.ModelSerializer):
    id = Base64UUIDField()

    class Meta:
        model = Organization
        fields = ('id',)


class TagRelationSerializer(serializers.ModelSerializer):
    id = Base64UUIDField()

    class Meta:
        model = Tag
        fields = ('id',)


class ProjectRelationSerializer(serializers.ModelSerializer):
    id = Base64UUIDField()

    class Meta:
        model = Project
        fields = ('id',)

class ProjectSerializer(serializers.ModelSerializer):

    startdate = serializers.DateField(format='%b %Y')
    enddate = serializers.DateField(format='%b %Y')
    tag = TagSerializer( many=True, read_only=True)
    organization = OrganizationRelationSerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'status', 'status_display', 'description', 'fulltimestaff', 'parttimestaff', 'startdate', 'enddate', 'organization', 'tag')

    def get_status_display(self, project):
        return project.get_status_display()


class ProjectSerializerForList(serializers.ModelSerializer):
    """
    Return a basic set of project info specifically for a read-only list
    """
    id = Base64UUIDField()
    organization = OrganizationRelationSerializer(many=True, read_only=True)
    tag = TagRelationSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'status', 'description', 'fulltimestaff', 'parttimestaff', 'startdate', 'enddate', 'organization', 'tag', 'id')



class OrganizationSerializerForList(serializers.ModelSerializer):
    """
    Return a basic set of project info specifically for a read-only list
    """
    id = Base64UUIDField()
    project_set = ProjectRelationSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'acronym', 'description', 'project_set', 'type', 'active')
