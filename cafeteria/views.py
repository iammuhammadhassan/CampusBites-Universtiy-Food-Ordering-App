from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import MenuItem, Order


def menu_list(request):
    """Display every menu item on the cafeteria menu."""
    items = MenuItem.objects.select_related("category")
    return render(request, "menu_list.html", {"items": items})


class MenuItemDetailView(DetailView):
    """Display the details for one menu item."""

    model = MenuItem
    template_name = "menu_detail.html"


class OrderListView(ListView):
    """Display all cafeteria orders with their related details."""

    model = Order
    template_name = "order_list.html"
    context_object_name = "orders"
    queryset = Order.objects.select_related("student__user", "meal").prefetch_related(
        "extras"
    )
