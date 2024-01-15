from django.urls import path

from . import views


app_name = 'ecom'


urlpatterns = [
    # products
    path('products/', views.ProductList.as_view(), name="product_list"),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name="product_detail"),
    path('products/<int:pk>/like/', views.LikeProduct.as_view(), name="product_like"),
    path('products/<int:pk>/unlike/', views.UnLikeProduct.as_view(), name="product_unlike"),
    # categories
    path('categories/', views.CategoryList.as_view(), name="category_list"),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name="category_detail"),
    # shops
    path('shops/', views.ShopList.as_view(), name="shop_list"),
    path('shops/<int:pk>/', views.ShopDetail.as_view(), name="shop_detail"),
    path('shops/<int:pk>/products/', views.ShopProduct.as_view(), name="shop_products"),
]