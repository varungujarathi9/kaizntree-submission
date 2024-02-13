from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    TAG_CHOICES = [
        ('ET', 'Etsy'),
        ('CT', 'In Shop'),
        ('ST', 'Settings'),
        ('OL', 'Online'),
        ('SP', 'Shopify'),
        ('SQ', 'Square'),
        ('XE', 'Xero')
    ]

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    SKU = models.CharField(max_length=100, blank=False)
    name = models.CharField(max_length=100, blank=False, unique=True)
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=100, choices=TAG_CHOICES)
    cost = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    in_stock = models.IntegerField(blank=False)
    available_stock = models.IntegerField(blank=False)
    minimum_stock = models.IntegerField(blank=False)
    desired_stock = models.IntegerField(blank=False)
    is_assembly = models.BooleanField(default=False)
    is_component = models.BooleanField(default=False)
    is_purchaseable = models.BooleanField(default=False)
    is_sellable = models.BooleanField(default=False)
    is_bundle = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, blank=True)
    created = models.DateTimeField(
        auto_now_add=True, auto_now=False, blank=True)
