import uuid

from rest_framework import serializers
import calendar
from django.utils import six
from rest_framework.fields import Field, UUIDField

from jsontag.models import Tag, ObjectTag
from project_tracker.uuidencode import uuid_to_base64, base64_to_uuid
from .models import Organization, OrganizationPlace, Project, ProjectPlace, Person, ProjectPerson, ProjectOrganization


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


class ProjectOrganizationRelationSerializer(serializers.ModelSerializer):
    # id = Base64UUIDField()
    organization = OrganizationRelationSerializer()
    class Meta:
        model = ProjectOrganization
        fields = ('organization','projectorganization')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('translation_id',)


class ObjectTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    class Meta:
        model = ObjectTag
        fields=('tag',)


class ProjectSerializer(serializers.ModelSerializer):

    class TagField(Field):
        def to_representation(self, value):
            return value.values_list('tag__translation_id', flat=True)

        def to_internal_value(self, data):
            pass

    startdate = serializers.DateField(format='iso-8601')
    enddate = serializers.DateField(format='iso-8601')
    projectorganization_set = ProjectOrganizationRelationSerializer(many=True, read_only=True)
    projectperson_set = ProjectPersonRelationSerializer(many=True, read_only=True)
    tag = ObjectTagSerializer(many=True)

    class Meta:
        model = Project
        fields = ('verified', 'modified','id', 'tag','name', 'status', 'description', 'fulltimestaff', 'parttimestaff', 'startdate', 'enddate', 'projectorganization_set', 'projectperson_set')


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
