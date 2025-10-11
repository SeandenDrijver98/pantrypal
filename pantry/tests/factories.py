from random import randint
from decimal import Decimal

from faker import Faker
from factory import LazyAttribute, SubFactory, post_generation
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User

from pantry.models import Ingredient, Recipe, Chef, Tag, UserSave, MealPlan, Food, FoodInventory

fake = Faker()


class UserFactory(DjangoModelFactory):
    """Factory for creating User instances"""
    
    username = LazyAttribute(lambda _: fake.user_name())
    email = LazyAttribute(lambda _: fake.email())
    first_name = LazyAttribute(lambda _: fake.first_name())
    last_name = LazyAttribute(lambda _: fake.last_name())
    
    class Meta:
        model = User


class FoodFactory(DjangoModelFactory):
    """Factory for creating Food instances"""
    
    name = LazyAttribute(lambda _: fake.word().title())
    
    class Meta:
        model = Food


class TagFactory(DjangoModelFactory):
    """Factory for creating Tag instances"""
    
    name = LazyAttribute(lambda _: fake.word().title())
    
    class Meta:
        model = Tag


class ChefFactory(DjangoModelFactory):
    """Factory for creating Chef instances"""
    
    name = LazyAttribute(lambda _: f"Chef {fake.name()}")
    avatar = LazyAttribute(lambda _: fake.image_url())
    specialty = LazyAttribute(lambda _: fake.catch_phrase())
    verified = LazyAttribute(lambda _: fake.boolean())
    followers = LazyAttribute(lambda _: fake.random_int(min=100, max=50000))
    recipes_count = LazyAttribute(lambda _: fake.random_int(min=5, max=200))
    rating = LazyAttribute(lambda _: Decimal(str(fake.random_int(min=35, max=50) / 10)))
    
    class Meta:
        model = Chef


class RecipeFactory(DjangoModelFactory):
    """Factory for creating Recipe instances"""
    
    name = LazyAttribute(lambda _: fake.catch_phrase())
    description = LazyAttribute(lambda _: fake.text(max_nb_chars=200))
    directions = LazyAttribute(lambda _: fake.text(max_nb_chars=500))
    calories = LazyAttribute(lambda _: fake.random_int(min=100, max=800))
    protein = LazyAttribute(lambda _: fake.random_int(min=5, max=50))
    prep_time = LazyAttribute(lambda _: fake.random_int(min=5, max=60))
    cook_time = LazyAttribute(lambda _: fake.random_int(min=10, max=120))
    servings = LazyAttribute(lambda _: fake.random_int(min=1, max=8))
    difficulty = LazyAttribute(lambda _: fake.random_element(elements=('easy', 'medium', 'hard')))
    image = LazyAttribute(lambda _: fake.image_url())
    rating = LazyAttribute(lambda _: Decimal(str(fake.random_int(min=30, max=50) / 10)))
    likes = LazyAttribute(lambda _: fake.random_int(min=0, max=1000))
    chef = SubFactory(ChefFactory)
    
    class Meta:
        model = Recipe


class IngredientFactory(DjangoModelFactory):
    """Factory for creating Ingredient instances"""
    
    food = SubFactory(FoodFactory)
    quantity = LazyAttribute(lambda _: fake.random_int(min=1, max=500))
    quantity_uom = LazyAttribute(lambda _: fake.random_element(elements=('g', 'kg', 'ml', 'l', 'tbsp', 'tsp', 'cup', 'pcs')))
    recipe = SubFactory(RecipeFactory)
    
    class Meta:
        model = Ingredient


class FoodInventoryFactory(DjangoModelFactory):
    """Factory for creating FoodInventory instances"""
    
    food = SubFactory(FoodFactory)
    quantity = LazyAttribute(lambda _: fake.random_int(min=100, max=2000))
    quantity_uom = LazyAttribute(lambda _: fake.random_element(elements=('g', 'kg', 'ml', 'l', 'tbsp', 'tsp', 'cup', 'pcs')))
    expiration_date = LazyAttribute(lambda _: fake.future_date())
    user = SubFactory(UserFactory)
    
    class Meta:
        model = FoodInventory


class UserSaveFactory(DjangoModelFactory):
    """Factory for creating UserSave instances"""
    
    user = SubFactory(UserFactory)
    recipe = SubFactory(RecipeFactory)
    
    class Meta:
        model = UserSave


class MealPlanFactory(DjangoModelFactory):
    """Factory for creating MealPlan instances"""
    
    user = SubFactory(UserFactory)
    recipe = SubFactory(RecipeFactory)
    planned_date = LazyAttribute(lambda _: fake.future_date())
    meal_type = LazyAttribute(lambda _: fake.random_element(elements=('breakfast', 'lunch', 'dinner', 'snack')))
    
    class Meta:
        model = MealPlan