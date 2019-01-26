import uuid

from django.db import models
from django.contrib.postgres import fields as pg
from django.utils import timezone
from django.conf import settings


class Profile(models.Model):
    """
    This model contains the profile data.
    Profiles represents the phisical profile data.
    It may be allways related to an user.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, verbose_name='First Name')
    last_name = models.CharField(max_length=150, verbose_name='Last Name')
    mothers_name = models.CharField(
        max_length=150, verbose_name="Mother's Name", null=True)
    fathers_name = models.CharField(
        max_length=150, verbose_name="Father's Name", null=True)
    phones = pg.JSONField(default=list)
    addresses = pg.JSONField(default=list)
    documents = pg.JSONField(default=list)
    birthdate = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_age(self):
        return timezone.now().year - self.birthdate.year
