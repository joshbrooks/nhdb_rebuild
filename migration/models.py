import uuid as uuid
from django.db import models

# Create your models here.

class IdToUUID(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    text_id = models.TextField()



class ProjectMigration(IdToUUID):
    pass

