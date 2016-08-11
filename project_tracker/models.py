from django.contrib.contenttypes.fields import GenericRelation
# from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from .uuidencode import base64_to_uuid, uuid_to_base64
from django.apps import apps

from unidecode import unidecode
import uuid

import logging
logger = logging.getLogger(__name__)

class ExcelDownloadFeedback(models.Model):

    PURPOSE_CHOICES = (
        ('PP', 'Project planning'),
        ('RE', 'Research'),
        ('IN', 'Personal interest'),
        ('OT', 'Other (please specify)'),
    )

    name = models.CharField(_('name'), max_length=150)
    organization = models.CharField(_('organization'), max_length=150)
    description = models.TextField(_('description'), null=True, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)
    purpose = models.CharField(max_length=2, choices=PURPOSE_CHOICES, )
    purposeother = models.CharField(_('Other purpose'), max_length=150, null=True, blank=True)
    referralurl = models.CharField(max_length=256, null=True, blank=True)


class Organization(models.Model):

    ORGANIZATION_TYPE_CHOICES = (
        ('LNGO', _('Local NGO')),
        ('INGO', _('International NGO')),
        ('CBO', _('Community-Based Organization')),
        ('GOV', _('Government (RDTL)')),
        ('IGOV', _('Government (overseas)')),
        ('UN', _('United Nations')),
        ('AC', _('Academic / Research Institute')),
        ('BI', _('Bilateral Agency'))
    )

    # Basic information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(_('name'), max_length=150)
    acronym = models.CharField(_('acronym'), max_length = 50, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    type = models.CharField(max_length = 10, verbose_name=_('Organization Type'), default="LNGO", choices=ORGANIZATION_TYPE_CHOICES, null=True, blank=True)
    active = models.BooleanField(default=True)

    # How many staff are in this organization
    fulltimestaff = models.IntegerField(null=True, blank=True, verbose_name="Full time staff")
    parttimestaff = models.IntegerField(null=True, blank=True, verbose_name="Part time staff")

    # Record the last modified date
    modified = models.DateField(null=True, blank=True, auto_now=True)
    verified = models.DateField(null=True, blank=True)


    # Links to JSON fields for more complicated relationships
    translation = GenericRelation('jsontag.Translation')
    contact = GenericRelation('jsontag.Contact')
    tag = GenericRelation('jsontag.Tag')
    history = GenericRelation('suggest.Change')


class Person(models.Model):

    class Meta:
        ordering = ['name']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True, blank=True)
    organization = models.ForeignKey('project_tracker.Organization', null=True, blank=True)
    contact = GenericRelation('jsontag.Contact')

    modified = models.DateField(auto_now=True, null=True, blank=True)
    verified = models.DateField(null=True, blank=True)
    history = GenericRelation('suggest.Change')


class RecordOwner(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.CharField(max_length=255)


class Project(models.Model):

    PROJECT_STATUS_CHOICES = (
        ('A', _('Active')),
        ('I', _('Inactive')),
        ('C', _('Cancelled')),
        ('P', _('Planned'))
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(_('name'), max_length=256, blank=True, null=True)
    description = models.TextField(null=True, blank=True, verbose_name=_("Project Description"))
    startdate = models.DateField(null=True, blank=True, verbose_name="Start date")
    enddate = models.DateField(null=True, blank=True, verbose_name="End date")
    verified = models.DateField(null=True, blank=True)
    modified = models.DateField(auto_now=True, null=True, blank=True)
    fulltimestaff = models.IntegerField(null=True, blank=True, verbose_name=_('Full time staff'))
    parttimestaff = models.IntegerField(null=True, blank=True, verbose_name=_('Part time staff'))

    status = models.CharField(max_length=1, verbose_name=_('ProjectStatus'), default='A', choices=PROJECT_STATUS_CHOICES)

    person = models.ManyToManyField(Person, through='ProjectPerson', blank=True)

    place = models.ManyToManyField('project_tracker.ProjectPlace', related_name="locations", blank=True)
    organization = models.ManyToManyField(Organization, through='ProjectOrganization', blank=True)

    # Links to JSON fields for more complicated relationships
    translation = GenericRelation('jsontag.Translation')
    contact = GenericRelation('jsontag.Contact')
    tag = GenericRelation('jsontag.ObjectTag', related_query_name='project')
    history = GenericRelation('suggest.Change')

    @classmethod
    def category_counts_active(cls):
        filter_params = {'objecttag__project__status':'A'}
        return cls.category_counts(filter_params)

    @classmethod
    def category_counts(cls, filter_params = None):

        tags = apps.get_model('jsontag.Tag').objects
        if filter_params:
            tags = tags.filter(**filter_params)
        else:
            tags = tags.filter(objecttag__project__status__isnull=False)
        tags = tags\
            .annotate(Count('objecttag__project')) \
            .values_list('objecttag__tag_id__translation__translation', 'objecttag__project__count')
        return tags

class ProjectOrganization(models.Model):

    PROJECT_ORGANIZATION_CHOICES = (
        ('P', 'Primary organization'),
        ('S', 'Secondary organization'),
        ('F', 'Funding organization'),
        ('O', 'Other'),
    )

    class Meta:
        verbose_name = "Project to Organization link"
        unique_together = (('project', 'organization'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    project = models.ForeignKey('Project')
    organization = models.ForeignKey(Organization, null=True, blank=True)
    projectorganization = models.CharField(max_length=1, choices=PROJECT_ORGANIZATION_CHOICES)
    notes = models.TextField(null=True, blank=True, verbose_name=_('Notes about this relationship'))


class ProjectPerson(models.Model):

    PROJECT_PERSON_CHOICES = (
        ('P', 'Primary contact'),
    )

    class Meta:
        unique_together = (('person', 'project'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    project = models.ForeignKey(Project)
    person = models.ForeignKey(Person)
    relationship = models.CharField(max_length=1, choices=PROJECT_PERSON_CHOICES, null=True, blank=True)
    verified = models.DateTimeField(null=True, blank=True)


class ProjectPlace(models.Model):

    class Meta:
        unique_together = (("project", "pcode"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    project = models.ForeignKey(Project)
    pcode = models.IntegerField()

    description = models.CharField(max_length=256, null=True, blank=True)


class OrganizationPlace(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    organization = models.ForeignKey('project_tracker.Organization', null=True, blank=False)
    description = models.CharField(max_length=256, null=True, blank=True)

    # point = models.PointField(srid=4326, null=True)
    suco = models.CharField(max_length=256, null=True, blank=True)
    subdistrict = models.CharField(max_length=256, null=True, blank=True)
    district = models.CharField(max_length=256, null=True, blank=True)
