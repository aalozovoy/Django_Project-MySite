
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ShopIndexView,
                    ProductListView,
                    GroupsListView,
                    ProductDetailsView,
                    OrdersListView,
                    OrdersDetailsView,
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDeleteView,
                    OrderCreateView,
                    OrderDeleteView,
                    OrderUpdateView,
                    ProductsExportView,
                    ProductViewSet,
                    OrderViewSet,
                    LatestProductsFeed)

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

app_name = "shopapp"
urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/export/", ProductsExportView.as_view(), name="products_export"),
    path("products/create/", ProductCreateView.as_view(), name="create_product"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete(archived)/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrdersListView.as_view(), name="order_list"),
    path("orders/create/", OrderCreateView.as_view(), name="create_order"),
    path("orders/<int:pk>/", OrdersDetailsView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("api/", include(routers.urls)),
    path("products/latest/feed/", LatestProductsFeed(), name="products-feed"),
]
