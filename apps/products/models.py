import uuid

from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    """
    This model contains the category data.
    Categories represents  the itens types.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name='Name', unique=True)
    description = models.TextField(
        max_length=150, verbose_name='Description', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    This model contains the product data.
    Products represents itens used on sales.
    It may allways contain a category.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150, verbose_name='Name', unique=True)
    description = models.TextField(
        max_length=150, verbose_name='Description', null=True, blank=True)
    purchase_price = models.DecimalField(
        max_digits=5, decimal_places=2)
    sale_price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def get_profit_per_item(self):
        return self.sale_price - self.purchase_price
