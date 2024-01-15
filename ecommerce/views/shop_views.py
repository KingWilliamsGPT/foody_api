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





class ShopList(ListCreateAPIView):
    '''The owner of the shop is assumed to be the logged in vendor, to create products for vendors as a staff use the admin dashboard
<br> Each shop name must be unique, even 'shop' and 'Shop' are NOT allowed
#### Note that
`Shop.is_manually_closed` is how you can manually close a shop
`Shop.is_closed` to know if a shop is closed either automaticaly or manually
`Shop.open_hour`, `Shop.open_hour` and `Shop.days_open` are used are used to automaticaly close the shop. check through `Shop.is_closed`
'''
    
    model = models.Shop
    serializer_class = serializers.ShopSearchSerializer
    queryset = model.objects.all()
    permission_classes = [HasGroupPermission]
    request = None

    def create(self, request, *a, **kw):
        self.request = request
        return super().create(request, *a, **kw)
    
    def perform_create(self, serializer):
        # ensure the product created only by
        serializer.save(owner=self.request.user)



class ShopDetail(RetrieveUpdateDestroyAPIView):
    model = models.Shop
    serializer_class = serializers.ShopSearchSerializer
    queryset = model.objects.all()
    permission_classes = [HasGroupPermission]
    request = None



class ShopProduct(ListCreateAPIView):
    pass

