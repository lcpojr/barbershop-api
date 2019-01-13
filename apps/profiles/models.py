import uuid
from django.db import models
from django.contrib.postgres import fields as pg
from django.utils import timezone
from django.conf import settings

class Person(models.Model):
    """
    This model contains the phisical person data.
    It may be allways related to an user
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, verbose_name='Full Name')
    mothers_name = models.CharField(max_length=150, verbose_name="Mother's Name", null=True)
    fathers_name = models.CharField(max_length=150, verbose_name="Father's Name", null=True)
    phones = pg.ArrayField(models.CharField(max_length=13))
    addresses = pg.ArrayField(pg.JSONField())
    documents = pg.ArrayField(pg.JSONField())
    birthdate = models.DateField()
    
    class Meta:
        verbose_name_plural = 'Person'

    def get_age(self):
        return timezone.now().year - self.birthdate.year