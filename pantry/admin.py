from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteTabularInline, ForeignKeyAutocompleteAdmin

from .models import Ingredient, Food, Recipe, FoodInventory, Tag


class IngredientInline(ForeignKeyAutocompleteTabularInline):
    model = Ingredient
    related_search_fields = {
        'food': ('name'),
    }
    extra = 1

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    search_fields = "name",

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = IngredientInline,


@admin.register(FoodInventory)
class FoodInventoryAdmin(ForeignKeyAutocompleteAdmin):
    search_fields = "food__name",
    related_search_fields = {
        'food': ('name'),
    }

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass