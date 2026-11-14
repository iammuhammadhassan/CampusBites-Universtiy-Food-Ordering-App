from django.contrib import admin

from .models import Category, Extra, MenuItem, Order, StudentProfile


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name",)


@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("roll_no", "user")
    search_fields = ("roll_no", "user__username")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("student", "meal", "size", "total", "created_at")
    list_filter = ("size", "created_at")
    search_fields = ("student__roll_no", "meal__name")
    filter_horizontal = ("extras",)
