from django.contrib import admin
from .models import Nutrient, NutrientValue, Ingredient, Food, Recipe

class NutrientValueInline(admin.TabularInline):
    model = NutrientValue
    extra = 1

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

@admin.register(Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    inlines = [NutrientValueInline]

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]


