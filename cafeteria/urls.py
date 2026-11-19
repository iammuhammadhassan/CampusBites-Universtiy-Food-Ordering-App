from django.urls import path

from .views import MenuItemDetailView, OrderListView, menu_list


urlpatterns = [
    path("", menu_list, name="home"),
    path("menu/<int:pk>/", MenuItemDetailView.as_view(), name="menu_detail"),
    path("orders/", OrderListView.as_view(), name="order_list"),
]
