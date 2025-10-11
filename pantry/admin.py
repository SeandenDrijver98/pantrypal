from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteTabularInline, ForeignKeyAutocompleteAdmin

from .models import Ingredient, Food, Recipe, FoodInventory, Tag, Chef, MealPlan, UserSave


class IngredientInline(ForeignKeyAutocompleteTabularInline):
    model = Ingredient
    related_search_fields = {
        'food': 'name',
    }
    extra = 1

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    search_fields = "name",

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = IngredientInline,
    list_display = ['name', 'difficulty', 'prep_time', 'cook_time', 'servings', 'rating', 'likes', 'chef']
    list_filter = ['difficulty', 'tags', 'chef']
    search_fields = ['name', 'description']


@admin.register(FoodInventory)
class FoodInventoryAdmin(ForeignKeyAutocompleteAdmin):
    search_fields = "food__name",
    related_search_fields = {
        'food': 'name',
    }

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'verified', 'followers', 'recipes_count', 'rating']
    list_filter = ['verified', 'specialty']
    search_fields = ['name', 'specialty']

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'planned_date', 'meal_type', 'created_at']
    list_filter = ['meal_type', 'planned_date', 'created_at']
    search_fields = ['user__username', 'recipe__name']

@admin.register(UserSave)
class UserSaveAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__username', 'recipe__name']