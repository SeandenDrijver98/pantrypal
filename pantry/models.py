from django.db import models


class Nutrient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class NutrientValue(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    value = models.FloatField()
    food = models.ForeignKey('Food', on_delete=models.CASCADE)


class Food(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=255)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.food.name}"

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Food)
    directions = models.TextField()

    def __str__(self):
        return self.name
