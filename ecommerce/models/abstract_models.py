import uuid

from django.db import models
from django.core import validators
from phonenumber_field.formfields import PhoneNumberField


import foodyapi.settings

from . import abstract_models


# These abstract classes are created basicaly because shop and users have similar related tables

class AbstractAddress(models.Model):
    # NOT COMPLETED

    class Meta:
        abstract = True


class AbstractPhoneNo(models.Model):
    number = PhoneNumberField()

    class Meta:
        abstract = True


class AbstractEmail(models.Model):
    email = models.EmailField()

    class Meta:
        abstract = True


class AbstractReview(models.Model):
    rating = models.IntegerField(validators=[validators.MinValueValidator(0.0), validators.MaxValueValidator(5.0)])
    review = models.CharField(max_length=2000)
    dateAdded = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    
    # Related Fields
    
    class Meta:
        abstract = True
