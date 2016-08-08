import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import ManyToManyField
from django.utils.translation import ugettext_lazy as _

from django.contrib.postgres.fields import JSONField
from django.db import models

class Translation(models.Model):
    """
    Stores an Object UUID and a JSONField translations field for that object's properties.
    """
    object_id = models.UUIDField(primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    translation = JSONField()

    @classmethod
    def set(cls, object_id, language_code='en', field_name='name', content='test'):
        generated_key = "{}_{}".format(field_name, language_code)
        translationobject = cls.objects.get_or_create(id=object_id)
        translationobject.translation[generated_key] = content
        translationobject.save()


class Contact(models.Model):
    """
    Stores an object UUID (project / organization) and Contact Details
    """
    CONTACT_METHODS = (
        ("P", _("Telephone")),
        ("E", _("Email")),
        ("W", _("Website")),
        ("F", _("Facebook")),
        ("X", _("Fax")),
    )
    object_id = models.UUIDField(primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    contact = JSONField()


class Tag(models.Model):

    object_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    translation = models.OneToOneField('jsontag.Translation')
    group = models.CharField(max_length=255)


class ObjectTag(models.Model):

    object_id = models.UUIDField(primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    tag_id = models.ForeignKey(Tag)