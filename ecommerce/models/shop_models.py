import uuid

from django.db import models
from django.core import validators
from phonenumber_field.formfields import PhoneNumberField
from django.utils.text import slugify


import foodyapi.settings


from . import abstract_models


class Shop(models.Model):
    # Days open - Using a Many-to-Many relationship to allow multiple days
    DAYS_CHOICES = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )

    # -- whats left

    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'^[\w\s-]+$',
                message='Shop name can only contain letters, numbers, spaces, or hyphens.',
                code='invalid_shop_name'
            )
        ]
    )
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True, editable=False)  # Add a SlugField

    description = models.CharField(max_length=1000, blank=True, default="")
    logo = models.ImageField(blank=True, null=True)
    dateAdded = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    # what's left
        # type of shop
        # shop_community
        # closing, opening times
        # pictures
    open_hour = models.TimeField(blank=True, null=True)
    close_hour = models.TimeField(blank=True, null=True)
    is_manually_closed = models.BooleanField(blank=True, default=False)
    days_open = models.JSONField(blank=True, null=True,  help_text='must be an array. eg. [1,2,3] -> ["monday", "tuesday", "wednesday"], Note: an empty array means open every day')
    # Related Fields

    # ONETOMANY
        # phone_numbers
        # emails
        # addresses: not completed needs google api stuff, 
                # according to chatgpt I need, django.contrib.gis.db.models for geospatial data to store addresses efficiently
        # ---
        # products
    # MANYTOONE
    owner = models.ForeignKey(foodyapi.settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shops')
    #MANYTOMANY
    

    def save(self, *args, **kwargs):
        # self.full_clean()  # Calls the clean() method

        # Auto-generate slug based on the shop name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"<Shop: name='{self.name}'>"


class ShopAddress(abstract_models.AbstractAddress):
    
    # Related Fields
    # MANYTOONE
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='addresses')


class ShopPhoneNo(abstract_models.AbstractPhoneNo):

    # Related Fields
    # MANYTOONE
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="phone_numbers")


class ShopEmail(abstract_models.AbstractEmail):
    email = models.EmailField()

    # Related Fields
    # MANYTOONE
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="emails")
