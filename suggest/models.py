import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models


class Change(models.Model):
    """
    Suggested change to a model
    """
    STATE_OPTIONS = (
        ('A', 'Accepted'),
        ('X', 'Rejected'),
        ('W', 'Waiting'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    object_id = models.UUIDField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    post = JSONField()

    creator = models.ForeignKey('auth.User', to_field='username', related_name='changes_created')
    auditor = models.ForeignKey('auth.User', to_field='username', related_name='changes_audited')

    created = models.DateField(null=True, blank=True, auto_now_add=True)
    modified = models.DateField(null=True, blank=True, auto_now=True)

    state = models.CharField(max_length=2, choices=STATE_OPTIONS)