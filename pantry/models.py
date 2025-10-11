from django.db import models
from django.contrib.auth.models import User

from pantry.constants import QUANTITY_UOM_CHOICES


class FoodInventory(models.Model):
    food = models.ForeignKey("Food", on_delete=models.CASCADE)
    quantity = models.FloatField()
    quantity_uom = models.CharField(max_length=255, default="g", choices=QUANTITY_UOM_CHOICES)
    expiration_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

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
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    directions = models.TextField()
    calories = models.PositiveIntegerField(default=0)
    protein = models.PositiveIntegerField(default=0)
    prep_time = models.PositiveIntegerField(default=0, help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(default=0, help_text="Cooking time in minutes")
    servings = models.PositiveIntegerField(default=1)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    image = models.URLField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    likes = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField("Tag", related_name="recipes")
    chef = models.ForeignKey("Chef", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tags"


class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    avatar = models.URLField(blank=True, null=True)
    specialty = models.CharField(max_length=255, blank=True)
    verified = models.BooleanField(default=False)
    followers = models.PositiveIntegerField(default=0)
    recipes_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    planned_date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'recipe', 'planned_date', 'meal_type']


class UserSave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'recipe']

class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)
    created_at = models.DateTimeField(auto_now_add=True)

class ShoppingListLine(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name="shopping_list_lines")
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField()
    quantity_uom = models.CharField(max_length=255, default="g", choices=QUANTITY_UOM_CHOICES)