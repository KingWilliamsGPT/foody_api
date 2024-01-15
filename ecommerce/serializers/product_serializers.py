from rest_framework import serializers

from .. import models


# - helpers ---------------------

def seriously_get_all_fields(model_klass):
    # used to get all fields DEFINED ON the model
    # do note that i'm removing trailing _id from the fields
    from django.db.models import Field
    from django.db.models.query_utils import DeferredAttribute
    from django.db.models.fields.related_descriptors import (ForwardManyToOneDescriptor,
                                                            ForwardOneToOneDescriptor, 
                                                            ReverseManyToOneDescriptor,
                                                            ReverseOneToOneDescriptor, 
                                                            ManyToManyDescriptor)

    fields = []
    model_klass = model_klass.__dict__
    remove_trailing_id =  lambda s: s[:-3] if s.endswith('_id') else s
    for key, thing in model_klass.items():
        try:
            if isinstance(thing, DeferredAttribute) and hasattr(thing, 'field'):
                if isinstance(thing.field, Field):
                    fields.append(remove_trailing_id(key))
            elif isinstance(thing, (Field, ForwardManyToOneDescriptor, ForwardOneToOneDescriptor, ReverseManyToOneDescriptor, ReverseOneToOneDescriptor, ManyToManyDescriptor)):
                fields.append(remove_trailing_id(key))
        except AttributeError:
            pass

    return fields


def remove(array, *stuff):
    # remove stuff from array
    for i in stuff:
        try:
            array.remove(i)
        except ValueError:
            pass

# - Serializers ---------------------

class IngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Ingredient
        fields = ('name', 'timestamp')


class ProductReview(serializers.ModelSerializer):

    class Meta:
        model = models.ProductReview
        fields = '__all__'


class BaseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'


class CategorySerializer(BaseCategorySerializer):

    def to_representation(self, instance):
        request = self.context.get('request')
        representation = super().to_representation(instance)

        representation['product_count'] = instance.products.filter(is_deleted=False).distinct().count()

        # trying to list all categories with their number of products in one query
        # queryset = instance.annotate(product_count=models.Count('products', filter=models.Q(products__is_deleted=False))) # un tested code i gess instance here should be a queryset
        # product_count = queryset.values_list('product_count', flat=True).first()
        return representation


class ProductSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        # exclude = ('favourite_users',)
        fields = seriously_get_all_fields(model)
        remove(fields, 'favourite_users', 'product_reviews')
    
    def to_representation(self, instance):
        request = self.context.get('request')
        representation = super().to_representation(instance)
        representation['discounted_price'] = instance.discounted_price

        if request is not None:
            representation['is_user_favourite'] = instance.is_user_favourite(request.user)
        
        return representation
    
    def validate_category(self, value):
        e = lambda t: {'detail': str(t)}
        if value is None:
            raise serializers.ValidationError("Please choose a category")

    def save(self, *a, **kw):
        # Extract category_id from the validated data or request
        category_id = self.validated_data.get('category', None) or self.context.get('request').data.get('category', None)

        # If category_id is available, set the category on the instance
        if category_id:
            category = models.Category.objects.get(pk=category_id)
            kw['category'] = category

        return super().save(*a, **kw)


class ProductDetailSerializer(ProductSearchSerializer):
    ingredients = IngredientSerializer(many=True, required=False)
    product_reviews = ProductReview(many=True, required=False)
    category = CategorySerializer(required=True)
    
    class Meta:
        model = models.Product
        # exclude = ('favourite_users',)
        fields = seriously_get_all_fields(model)
        fields.remove('favourite_users')