from django.db import models

from pantry.constants import QUANTITY_UOM_CHOICES


class FoodInventory(models.Model):
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
    tags = models.ManyToManyField("Tag", related_name="recipes", null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tags"