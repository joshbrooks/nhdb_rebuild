import uuid

from rest_framework import serializers
import calendar
from django.utils import six
from rest_framework.fields import Field, UUIDField

from project_tracker.uuidencode import uuid_to_base64, base64_to_uuid
from .models import Organization, OrganizationPlace, Project, ProjectPlace, Person, ProjectPerson


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [field.name for field in model._meta.fields]


class Base64UUIDField(Field):

    def to_internal_value(self, data):
        # return data
        return base64_to_uuid(data)

    def to_representation(self, value):
        # return value
        return uuid_to_base64(value).decode().strip('=')


class OrganizationRelationSerializer(serializers.ModelSerializer):
    # id = Base64UUIDField()

    class Meta:
        model = Organization
        fields = ('id','name')


class ProjectRelationSerializer(serializers.ModelSerializer):
    # id = Base64UUIDField()

    class Meta:
        model = Project

        fields = ('id','name')


class PersonRelationSerializer(serializers.ModelSerializer):
    # id = Base64UUIDField()

    class Meta:
        model = Person
        fields = ('id','name')


class ProjectPersonRelationSerializer(serializers.ModelSerializer):
    # id = Base64UUIDField()
    person = PersonRelationSerializer()
    class Meta:
        model = ProjectPerson
        fields = ('person','relationship')


class ProjectSerializer(serializers.ModelSerializer):

    startdate = serializers.DateField(format='iso-8601')
    enddate = serializers.DateField(format='iso-8601')
    organization = OrganizationRelationSerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField()
    # projectperson_set = ProjectPersonRelationSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'status', 'status_display', 'description', 'fulltimestaff', 'parttimestaff', 'startdate', 'enddate', 'organization', 'projectperson_set')

    def get_status_display(self, project):
        return project.get_status_display()


class ProjectSerializerForList(serializers.ModelSerializer):
    """
    Return a basic set of project info specifically for a read-only list
    """
    id = Base64UUIDField()
    organization = OrganizationRelationSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'status', 'description', 'fulltimestaff', 'parttimestaff', 'startdate', 'enddate', 'organization', 'id')



class OrganizationSerializerForList(serializers.ModelSerializer):
    """
    Return a basic set of project info specifically for a read-only list
    """
    id = Base64UUIDField()
    project_set = ProjectRelationSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'acronym', 'description', 'project_set', 'type', 'active')


class PersonSerializer(serializers.ModelSerializer):
    project_set = ProjectRelationSerializer(many=True, read_only=True)
    organization = OrganizationRelationSerializer()
    class Meta:
        model = Person
        fields = ('id', 'name', 'title', 'organization', 'modified', 'verified', 'project_set')
