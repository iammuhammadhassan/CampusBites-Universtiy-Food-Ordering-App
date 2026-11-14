from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
    )  # A menu item belongs to its category.
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (PKR {self.price})"


class Extra(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (PKR {self.price})"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )  # A profile is removed when its Django user is removed.
    roll_no = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.roll_no} - {self.user.get_full_name() or self.user.username}"


class Order(models.Model):
    REGULAR = "Regular"
    LARGE = "Large"
    SIZE_CHOICES = [
        (REGULAR, "Regular"),
        (LARGE, "Large"),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="orders",
    )  # A student's orders are removed with the student profile.
    meal = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
        related_name="orders",
    )  # Protect menu items so existing order history remains valid.
    extras = models.ManyToManyField(Extra, blank=True)  # An order can include multiple extras.
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.meal.name} ({self.size})"
