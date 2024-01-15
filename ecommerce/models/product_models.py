from decimal import Decimal

import uuid

from django.db import models
from django.core import validators
from phonenumber_field.formfields import PhoneNumberField


import foodyapi.settings

from . import abstract_models


class Product(models.Model):
    # Unique Identifiers
    productID = models.UUIDField(default=uuid.uuid4, editable=False)                    # this uniquely identifies the product without exposing the database structure
                                                                                        # will be used to encode qr code
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)                                                         # be cautious how you use price to avoid zerodivition
    discount = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2, validators=[validators.MinValueValidator(0.0), validators.MaxValueValidator(1.0)])
    unitPlural = models.CharField(max_length=20, default="quantities")                 # plural of the product

    videoURL = models.URLField(blank=True, default="")
    
    # edited on a rating
    average_rating = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2, validators=[validators.MinValueValidator(0.0), validators.MaxValueValidator(5.0)], editable=False)          # null rating means not rated
    
    # edited on an order
    orderCount = models.IntegerField(blank=True, default=0, editable=False)
    isBestSelling = models.BooleanField(blank=True, default=False, editable=False)

    is_deleted = models.BooleanField(blank=True, default=False)
    dateAdded = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    # what's left
    # orders

    # Related Fields
    #ONETOONE
    productImages = models.OneToOneField('ProductSlide', on_delete=models.CASCADE, blank=True, null=True)   # must have exactly one row even if all the images are left blank

    #MANYTOONE
    # it does'nt make sence to keep refernce to shop, when menu has it
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='products', null=True)
    # menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='products')
    # lastUpdatedBy = models.ForeignKey(foodyapi.settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # createdBy = models.ForeignKey(foodyapi.settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    #ONETOMANY
    # ingredients, product_reviews, orders

    #MANYTOMANY
    favourite_users = models.ManyToManyField(foodyapi.settings.AUTH_USER_MODEL, related_name="favourite_products")

    class Meta:
        unique_together = ('shop', 'name')           # One product should't have duplicate ingredients

    def is_user_favourite(self, user):
        # check if logged in user is ammong favourite users
        if user.is_authenticated:
            return user in self.favourite_users.all()
        return False

    @property
    def discounted_price(self):
        if self.discount:
            price = Decimal(self.price)
            return price - price * self.discount      # note: discounted price is not necessary selling price
        return self.price

    def __str__(self):
        return f"<Product: name='{self.name}'>"


class Category(models.Model):
    """
    Model representing a category for items in the app.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=1000, blank=True, default="")


    def __str__(self):
        return f'<Category: {self.name}>'


class ProductSlide(models.Model):
    """Images for the product."""
    main = models.ImageField(blank=True, null=True)
    pic1 = models.ImageField(blank=True, null=True)
    pic2 = models.ImageField(blank=True, null=True)
    pic3 = models.ImageField(blank=True, null=True)



class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Related Fields
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients')

    class Meta:
        ordering = ('-timestamp',)
        unique_together = ('product', 'name')           # One product should't have duplicate ingredients


class ProductReview(abstract_models.AbstractReview):
    # Related Fields
    # MANYTOONE
    owner = models.ForeignKey(foodyapi.settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="product_reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_reviews")

    class Meta:
        unique_together = ('product', 'owner')      # this ensures users can only rate a product once, editable though.
                                                    # i.e there are no two review instances with the same product and product_reveiw
                                                    # i.e a product with multiple reviews from the same user