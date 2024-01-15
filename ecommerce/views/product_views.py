from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, CreateAPIView, ListCreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


from .. import models
from .. import serializers
from ..perm import HasGroupPermission




class ProductList(ListCreateAPIView):
    '''This is a primitive search that searches in the product's name, description, and ingredients
    <br> Query Params `?query=[SERCH_ITEM]&?category_id=[CATEGORY_ID]?vendor_id=[VENDOR_ID]`
    <br>
### How to use
```python
# search all products
products/
products/?query=potato

# search product in a category
products/?query=potota&category_id=5

# search product in a shop
products/?query=potota&shop_id=5

# search product owned by a vendor
products/?query=potota&vendor_id=5

# Any combination above can still work
# eg. search the products, in a shop, in a specific category

products/?query=pototo&shop_id=5&category=2
```
'''
    
    model = models.Product
    serializer_class = serializers.ProductSearchSerializer
    queryset = model.objects.exclude(is_deleted__exact=True)

    permission_classes = [HasGroupPermission]

    def get_queryset(self):
        qset = super().get_queryset()
        query = self.request.GET.get('query')
        category = self.request.GET.get('category_id')
        vendor = self.request.GET.get('vendor_id')
        shop = self.request.GET.get('shop_id')

        if shop:
            qset = qset.filter(shop__id=shop)

        if vendor:
            qset = qset.filter(shop__owner__id=vendor)

        if category:
            qset = qset.filter(category__id=category)

        if query:
            qset = qset.filter(
                Q(name__icontains=query) |
                # Q(price__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredients__name__icontains=query)
            )
        # else:
        #     qset = self.queryset.all()

        return qset.distinct()


class ProductDetail(RetrieveUpdateDestroyAPIView):
    '''**Full description of the product.**'''
    
    model = models.Product
    queryset = model.objects.all()
    serializer_class = serializers.ProductDetailSerializer
    permission_classes = [HasGroupPermission]


    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
   


class LikeProduct(RetrieveAPIView):
    '''**Just adds the product to users favourites**'''
    
    model = models.Product
    queryset = model.objects.all()
    serializer_class = serializers.ProductDetailSerializer
    permission_classes = [HasGroupPermission]

    def get(self, request, pk):
        try:
            product = self.queryset.get(pk=pk)
            product.favourite_users.add(request.user)
        except self.model.DoesNotExist:
            pass
        return super().get(request, pk)


class UnLikeProduct(RetrieveAPIView):
    '''**Just adds the product to users favourites**'''
    
    model = models.Product
    queryset = model.objects.all()
    serializer_class = serializers.ProductDetailSerializer
    permission_classes = [HasGroupPermission]

    def get(self, request, pk):
        try:
            product = self.queryset.get(pk=pk)
            product.favourite_users.remove(request.user)
        except self.model.DoesNotExist:
            pass
        return super().get(request, pk)




# Categories

class CategoryList(ListCreateAPIView):
    model = models.Category
    queryset = model.objects.all()
    serializer_class = serializers.BaseCategorySerializer
    permission_classes = [HasGroupPermission]


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    model = models.Category
    queryset = model.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [HasGroupPermission]





footer = '''\
<br> Products with `is_deleted=False` don't show up.
<br> Search is not based on Location yet.
<br> Pagination size is set to 5 so you can test pagination. Create more than 5 items to see
<br> Errors look like
<br> 
```json

    {
        "detail": "Error Message eg. You do not have permission to perform this action."
    }
```
    '''

_g = globals().copy()
for k, thing in _g.items():
    if hasattr(thing, '__mro__') and APIView in thing.__mro__:
        thing.__doc__ = thing.__doc__ or ' '
        thing.__doc__ += footer