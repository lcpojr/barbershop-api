import uuid

from django.db import models
from django.contrib.postgres import fields as pg
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator

from apps.profiles.models import Profile
from apps.products.models import Product


class ProductItem(models.Model):
    """
    This model contains the itens product data.
    Product itens represents consumible products.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Product Item'
        verbose_name_plural = 'Product Itens'

    def __str__(self):
        return "{} ({}) - R$ {}".format(self.item.name, self.quantity, self.get_total())

    def get_total(self):
        return self.item.sale_price * self.quantity


class Sale(models.Model):
    """
    This model contains the sale data.
    Sales represents transactions data.
    It may contain services or products.
    """

    TRANSACTION_STATUS = (
        ('open', 'Open'),
        ('waiting', 'Waiting Payment'),
        ('canceled', 'Canceled'),
        ('payed', 'Payed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, related_name='profile_client')
    employe = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, null=True, related_name='profile_employe')
    products = models.ManyToManyField(ProductItem)
    status = models.CharField(
        max_length=8, choices=TRANSACTION_STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Sales'

    def __str__(self):
        return "{} ({}) - R$ {}".format(self.client.full_name, self.updated_at, self.get_total())

    def get_total(self):
        total = 0
        for product in self.products.all():
            total += product.get_total()
        return total

    def get_client_name(self):
        return self.client.full_name

    def get_employe_name(self):
        if self.employe:
            return self.employe.full_name
        else:
            return None
