from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from pantry.constants import QUANTITY_UOM_CHOICES

class UserManager(BaseUserManager):
    """
    Define a model manager for User model with no username field.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)

    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self) -> str:
        return f"{self.get_full_name()} ({self.email})"


class FoodInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey("Food", on_delete=models.CASCADE)
    quantity = models.FloatField()
    quantity_uom = models.CharField(max_length=255, default="g", choices=QUANTITY_UOM_CHOICES)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} {self.quantity_uom} {self.food.name}"

    class Meta:
        verbose_name_plural = "Food Inventories"


class Food(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    quantity = models.FloatField()
    quantity_uom = models.CharField(max_length=255, default="grams")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.quantity} {self.quantity_uom} {self.food.name}"


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    directions = models.TextField()
    calories = models.PositiveIntegerField(default=0)
    protein = models.PositiveIntegerField( default=0)
    tags = models.ManyToManyField("Tag", related_name="recipes")
    url = models.URLField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tags"